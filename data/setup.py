#!/usr/bin/env python3
"""
Seed script: downloads Kickstarter CSV via Kaggle CLI (or accepts --csv path),
normalizes into 5 SQLite tables, and creates the v_campaign_info view.

Usage:
    uv run python data/setup.py                   # download from Kaggle
    uv run python data/setup.py --csv <path>      # use local CSV
"""

import argparse
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pandas as pd

DB_PATH = Path(__file__).parent / "kickstarter.db"
DATA_DIR = Path(__file__).parent

# Currency conversion rates (xe.com, 11/06/2022)
# Keys match the currency name strings in the CSV
CURRENCY_RATES = {
    "GBP": 1.23,
    "USD": 1.00,
    "AUD": 0.78,
    "CAD": 0.79,
    "EUR": 1.05,
    "NOK": 0.10,
    "SEK": 0.10,
    "DKK": 0.14,
    "CHF": 1.06,
    "NZD": 0.64,
    "SGD": 0.74,
    "HKD": 0.13,
    "MXN": 0.05,
}


def download_dataset() -> Path:
    csv_path = DATA_DIR / "ks-projects-201801.csv"
    if csv_path.exists():
        print(f"  CSV already present: {csv_path}")
        return csv_path

    print("  Downloading Kickstarter dataset from Kaggle...")
    result = subprocess.run(
        [
            "kaggle",
            "datasets", "download",
            "-d", "kemical/kickstarter-projects",
            "--unzip",
            "-p", str(DATA_DIR),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"  Kaggle download failed:\n{result.stderr}")
        sys.exit(1)

    # Kaggle may unzip to slightly different filename; find the CSV
    candidates = list(DATA_DIR.glob("ks-projects*.csv"))
    if not candidates:
        print("  No CSV found after download.")
        sys.exit(1)
    return candidates[0]


def build_database(csv_path: Path) -> None:
    print(f"  Reading CSV: {csv_path}")
    df = pd.read_csv(csv_path, encoding="utf-8", low_memory=False)
    print(f"  Loaded {len(df):,} rows, columns: {list(df.columns)}")

    # Normalise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # Rename columns to match expected names
    rename_map = {
        "id": "id",
        "name": "name",
        "category": "sub_category_name",
        "main_category": "category_name",
        "currency": "currency_name",
        "deadline": "deadline",
        "goal": "goal",
        "launched": "launched",
        "pledged": "pledged",
        "state": "outcome",
        "backers": "backers",
        "country": "country_name",
        "usd_pledged": "usd_pledged_old",
        "usd_pledged_real": "usd_pledged_real",
        "usd_goal_real": "usd_goal_real",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Drop duplicate IDs — keep first occurrence
    df = df.drop_duplicates(subset=["id"])

    print("  Building lookup tables...")

    # --- currency ---
    currencies = (
        pd.DataFrame({"name": sorted(df["currency_name"].dropna().unique())})
        .reset_index(drop=True)
    )
    currencies.index += 1
    currencies.index.name = "id"
    currencies = currencies.reset_index()

    # --- country ---
    countries = (
        pd.DataFrame({"name": sorted(df["country_name"].dropna().unique())})
        .reset_index(drop=True)
    )
    countries.index += 1
    countries.index.name = "id"
    countries = countries.reset_index()

    # --- category ---
    categories = (
        pd.DataFrame({"name": sorted(df["category_name"].dropna().unique())})
        .reset_index(drop=True)
    )
    categories.index += 1
    categories.index.name = "id"
    categories = categories.reset_index()

    cat_name_to_id = dict(zip(categories["name"], categories["id"]))

    # --- sub_category ---
    sub_cat_df = (
        df[["sub_category_name", "category_name"]]
        .dropna()
        .drop_duplicates()
        .sort_values("sub_category_name")
        .reset_index(drop=True)
    )
    sub_cat_df.index += 1
    sub_cat_df.index.name = "id"
    sub_cat_df = sub_cat_df.reset_index()
    sub_cat_df["category_id"] = sub_cat_df["category_name"].map(cat_name_to_id)
    sub_categories = sub_cat_df[["id", "sub_category_name", "category_id"]].rename(
        columns={"sub_category_name": "name"}
    )

    sub_cat_name_to_id = dict(zip(sub_cat_df["sub_category_name"], sub_cat_df["id"]))
    cur_name_to_id = dict(zip(currencies["name"], currencies["id"]))
    ctry_name_to_id = dict(zip(countries["name"], countries["id"]))

    # --- campaign ---
    print("  Mapping campaign FK IDs...")
    df["sub_category_id"] = df["sub_category_name"].map(sub_cat_name_to_id)
    df["currency_id"] = df["currency_name"].map(cur_name_to_id)
    df["country_id"] = df["country_name"].map(ctry_name_to_id)

    # Normalise outcome
    df["outcome"] = df["outcome"].str.lower().str.strip()

    campaign_cols = [
        "id", "name", "goal", "pledged", "backers", "outcome",
        "launched", "deadline", "sub_category_id", "country_id", "currency_id",
    ]
    campaign = df[campaign_cols].copy()

    # Coerce numeric columns
    for col in ["goal", "pledged", "backers"]:
        campaign[col] = pd.to_numeric(campaign[col], errors="coerce")

    campaign = campaign.dropna(subset=["sub_category_id", "currency_id", "country_id"])
    print(f"  Campaign rows after FK cleaning: {len(campaign):,}")

    # --- Write to SQLite ---
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("  Removed existing DB.")

    print(f"  Writing to {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)

    currencies.to_sql("currency", conn, index=False, if_exists="replace")
    countries.to_sql("country", conn, index=False, if_exists="replace")
    categories.to_sql("category", conn, index=False, if_exists="replace")
    sub_categories.to_sql("sub_category", conn, index=False, if_exists="replace")
    campaign.to_sql("campaign", conn, index=False, if_exists="replace")

    # --- Build currency rate lookup table ---
    rate_rows = [(cur_name_to_id[k], k, v) for k, v in CURRENCY_RATES.items() if k in cur_name_to_id]
    conn.execute("DROP TABLE IF EXISTS currency_rate")
    conn.execute(
        "CREATE TABLE currency_rate (currency_id INTEGER, currency_name TEXT, usd_rate REAL)"
    )
    conn.executemany("INSERT INTO currency_rate VALUES (?,?,?)", rate_rows)

    # --- Create views ---
    print("  Creating views...")
    conn.execute("DROP VIEW IF EXISTS v_campaign_info")
    conn.execute(
        """
        CREATE VIEW v_campaign_info AS
        SELECT c.*
        FROM campaign c
        WHERE c.outcome IN ('successful', 'failed')
          AND NOT (c.backers = 0 AND c.pledged > 0)
          AND c.country_id != 17
        """
    )

    conn.execute("DROP VIEW IF EXISTS v_condensed")
    conn.execute(
        """
        CREATE VIEW v_condensed AS
        WITH durations AS (
            SELECT id,
                   (julianday(deadline) - julianday(launched)) AS days
            FROM campaign
        )
        SELECT
            c.id,
            c.name,
            c.sub_category_id,
            c.country_id,
            c.currency_id,
            c.outcome,
            c.backers,
            ROUND(d.days) AS days,
            ROUND(c.goal * COALESCE(cr.usd_rate, 1.0), 2) AS USD_goal,
            ROUND(c.pledged * COALESCE(cr.usd_rate, 1.0), 2) AS USD_pledged
        FROM v_campaign_info c
        JOIN durations d ON c.id = d.id
        LEFT JOIN currency_rate cr ON c.currency_id = cr.currency_id
        """
    )

    conn.commit()

    # --- Counts ---
    cur = conn.cursor()
    for tbl in ["currency", "country", "category", "sub_category", "campaign"]:
        n = cur.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"    {tbl}: {n:,} rows")

    n_view = cur.execute("SELECT COUNT(*) FROM v_campaign_info").fetchone()[0]
    print(f"    v_campaign_info: {n_view:,} rows")

    conn.close()
    print(f"\n  DB created: {n_view:,} campaigns loaded into v_campaign_info")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Kickstarter SQLite DB")
    parser.add_argument("--csv", type=Path, default=None, help="Path to ks-projects-201801.csv")
    args = parser.parse_args()

    print("=== Kickstarter DB Setup ===")
    csv_path = args.csv if args.csv else download_dataset()
    build_database(csv_path)
    print("Done.")


if __name__ == "__main__":
    main()
