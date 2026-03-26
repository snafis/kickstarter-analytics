# All SQL queries as named constants.
# SQLite-compatible (no MySQL-specific syntax).

# ── Views ──────────────────────────────────────────────────────────────────────

VIEW_CAMPAIGN_INFO = """
SELECT c.*
FROM campaign c
WHERE c.outcome IN ('successful', 'failed')
  AND NOT (c.backers = 0 AND c.pledged > 0)
  AND c.country_id != (
      SELECT id FROM country WHERE name = 'N,0"'
  )
"""

# v_condensed: cleaned campaigns with USD-normalised goal/pledged and duration
VIEW_CONDENSED = """
WITH durations AS (
    SELECT id,
           (julianday(deadline) - julianday(launched)) AS days
    FROM campaign
),
base AS (
    SELECT c.*
    FROM campaign c
    WHERE c.outcome IN ('successful', 'failed')
      AND NOT (c.backers = 0 AND c.pledged > 0)
      AND c.country_id != (
          SELECT id FROM country WHERE name = 'N,0"'
      )
)
SELECT
    b.id,
    b.name,
    b.sub_category_id,
    b.country_id,
    b.currency_id,
    b.outcome,
    b.backers,
    ROUND(d.days) AS days,
    ROUND(b.goal  * COALESCE(cr.usd_rate, 1.0), 2) AS USD_goal,
    ROUND(b.pledged * COALESCE(cr.usd_rate, 1.0), 2) AS USD_pledged
FROM base b
JOIN durations d ON b.id = d.id
LEFT JOIN currency_rate cr ON b.currency_id = cr.currency_id
"""

# ── Data quality checks ────────────────────────────────────────────────────────

QC_ALL_OUTCOMES = """
SELECT outcome, COUNT(*) AS campaign_count
FROM campaign
GROUP BY outcome
ORDER BY campaign_count DESC
"""

QC_EXPLORE_CURRENCIES = """
SELECT cu.name AS currency, COUNT(*) AS campaign_count
FROM campaign c
JOIN currency cu ON c.currency_id = cu.id
GROUP BY cu.name
ORDER BY campaign_count DESC
"""

QC_ZERO_BACKERS_WITH_PLEDGED = """
SELECT COUNT(*) AS anomalous_rows
FROM campaign
WHERE backers = 0 AND pledged > 0
"""

QC_COUNTRY_ANOMALY = """
SELECT co.name AS country, COUNT(*) AS campaign_count
FROM campaign c
JOIN country co ON c.country_id = co.id
GROUP BY co.name
ORDER BY campaign_count DESC
"""

QC_ALL_CATEGORIES = """
SELECT cat.name AS category,
       COUNT(DISTINCT s.id) AS subcategory_count,
       COUNT(c.id) AS campaign_count
FROM category cat
JOIN sub_category s ON s.category_id = cat.id
JOIN campaign c ON c.sub_category_id = s.id
GROUP BY cat.name
ORDER BY campaign_count DESC
"""

QC_SAMPLE_CAMPAIGNS = """
SELECT c.id, c.name, c.outcome, c.goal, c.pledged, c.backers,
       s.name AS sub_category, cat.name AS category,
       co.name AS country, cu.name AS currency,
       c.launched, c.deadline
FROM campaign c
JOIN sub_category s ON c.sub_category_id = s.id
JOIN category cat ON s.category_id = cat.id
JOIN country co ON c.country_id = co.id
JOIN currency cu ON c.currency_id = cu.id
LIMIT 50
"""

# ── Analysis queries ───────────────────────────────────────────────────────────

Q1_OUTCOME_AVERAGES = """
WITH condensed AS (
    %(condensed)s
)
SELECT
    outcome,
    ROUND(AVG(USD_goal), 2)     AS avg_goal_usd,
    ROUND(AVG(USD_pledged), 2)  AS avg_pledged_usd,
    ROUND(AVG(backers), 0)      AS avg_backers,
    COUNT(*)                    AS campaign_count
FROM condensed
GROUP BY outcome
ORDER BY outcome DESC
""" % {"condensed": VIEW_CONDENSED}

Q2_TOP_CATEGORIES_BACKERS = """
WITH condensed AS (%(condensed)s),
cat_stats AS (
    SELECT cat.name AS category,
           SUM(con.backers) AS total_backers,
           (SUM(con.backers) / COUNT(*)) AS avg_backers
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    JOIN category cat ON s.category_id = cat.id
    GROUP BY cat.name
)
SELECT * FROM cat_stats ORDER BY total_backers DESC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q2_BOTTOM_CATEGORIES_BACKERS = """
WITH condensed AS (%(condensed)s),
cat_stats AS (
    SELECT cat.name AS category,
           SUM(con.backers) AS total_backers,
           (SUM(con.backers) / COUNT(*)) AS avg_backers
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    JOIN category cat ON s.category_id = cat.id
    GROUP BY cat.name
)
SELECT * FROM cat_stats ORDER BY total_backers ASC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q2_TOP_SUBCATEGORIES_BACKERS = """
WITH condensed AS (%(condensed)s),
sub_stats AS (
    SELECT s.name AS sub_category,
           SUM(con.backers) AS total_backers,
           (SUM(con.backers) / COUNT(*)) AS avg_backers
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    GROUP BY s.name
)
SELECT * FROM sub_stats ORDER BY total_backers DESC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q2_BOTTOM_SUBCATEGORIES_BACKERS = """
WITH condensed AS (%(condensed)s),
sub_stats AS (
    SELECT s.name AS sub_category,
           SUM(con.backers) AS total_backers,
           (SUM(con.backers) / COUNT(*)) AS avg_backers
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    GROUP BY s.name
)
SELECT * FROM sub_stats ORDER BY total_backers ASC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q3_TOP_CATEGORIES_MONEY = """
WITH condensed AS (%(condensed)s),
cat_stats AS (
    SELECT cat.name AS category,
           ROUND(SUM(con.USD_pledged), 2) AS total_raised,
           ROUND(SUM(con.USD_pledged) / COUNT(*), 2) AS avg_raised
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    JOIN category cat ON s.category_id = cat.id
    GROUP BY cat.name
)
SELECT * FROM cat_stats ORDER BY total_raised DESC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q3_BOTTOM_CATEGORIES_MONEY = """
WITH condensed AS (%(condensed)s),
cat_stats AS (
    SELECT cat.name AS category,
           ROUND(SUM(con.USD_pledged), 2) AS total_raised,
           ROUND(SUM(con.USD_pledged) / COUNT(*), 2) AS avg_raised
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    JOIN category cat ON s.category_id = cat.id
    GROUP BY cat.name
)
SELECT * FROM cat_stats ORDER BY total_raised ASC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q3_TOP_SUBCATEGORIES_MONEY = """
WITH condensed AS (%(condensed)s),
sub_stats AS (
    SELECT s.name AS sub_category,
           ROUND(SUM(con.USD_pledged), 2) AS total_raised,
           ROUND(SUM(con.USD_pledged) / COUNT(*), 2) AS avg_raised
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    GROUP BY s.name
)
SELECT * FROM sub_stats ORDER BY total_raised DESC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q3_BOTTOM_SUBCATEGORIES_MONEY = """
WITH condensed AS (%(condensed)s),
sub_stats AS (
    SELECT s.name AS sub_category,
           ROUND(SUM(con.USD_pledged), 2) AS total_raised,
           ROUND(SUM(con.USD_pledged) / COUNT(*), 2) AS avg_raised
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    GROUP BY s.name
)
SELECT * FROM sub_stats ORDER BY total_raised ASC LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q4_BEST_TABLETOP_GAME = """
WITH condensed AS (%(condensed)s),
top_boardgame AS (
    SELECT con.id,
           con.backers,
           ROUND(con.USD_pledged, 2) AS USD_pledged,
           ROUND(con.USD_goal, 2) AS USD_goal,
           ROUND(con.USD_pledged / con.backers, 2) AS avg_pledge_per_backer
    FROM condensed con
    JOIN sub_category s ON con.sub_category_id = s.id
    WHERE LOWER(s.name) LIKE '%%tabletop%%'
      AND con.outcome = 'successful'
    ORDER BY con.USD_pledged DESC
    LIMIT 1
)
SELECT c.name, t.id, t.backers, t.USD_pledged, t.USD_goal, t.avg_pledge_per_backer
FROM top_boardgame t
JOIN campaign c ON t.id = c.id
""" % {"condensed": VIEW_CONDENSED}

Q5_TOP_COUNTRIES = """
WITH condensed AS (%(condensed)s)
SELECT
    co.name AS country,
    COUNT(*) AS number_of_campaigns,
    ROUND(SUM(con.USD_pledged), 2) AS total_pledged,
    ROUND(SUM(con.USD_pledged) / COUNT(*), 2) AS avg_pledged,
    SUM(con.backers) AS total_backers
FROM condensed con
JOIN country co ON co.id = con.country_id
WHERE con.outcome = 'successful'
GROUP BY country
ORDER BY total_pledged DESC
LIMIT 3
""" % {"condensed": VIEW_CONDENSED}

Q6_DURATION_IMPACT = """
WITH condensed AS (%(condensed)s)
SELECT
    CAST(days AS INTEGER) AS duration,
    ROUND(AVG(USD_pledged), 2) AS avg_raised,
    COUNT(*) AS campaign_count
FROM condensed
WHERE days BETWEEN 1 AND 92
GROUP BY duration
ORDER BY duration
""" % {"condensed": VIEW_CONDENSED}

# ── Visualization data queries ─────────────────────────────────────────────────

VIZ_SCATTER_DATA = """
WITH condensed AS (%(condensed)s)
SELECT
    ROUND(USD_goal, 2) AS USD_goal,
    ROUND(USD_pledged, 2) AS USD_pledged,
    outcome
FROM condensed
WHERE USD_goal > 0 AND USD_pledged >= 0
""" % {"condensed": VIEW_CONDENSED}

VIZ_GOAL_HISTOGRAM = """
WITH condensed AS (%(condensed)s)
SELECT
    ROUND(USD_goal, 2) AS USD_goal,
    outcome
FROM condensed
WHERE USD_goal BETWEEN 1 AND 500000
ORDER BY outcome
""" % {"condensed": VIEW_CONDENSED}

VIZ_CATEGORY_PERFORMANCE = """
WITH condensed AS (%(condensed)s)
SELECT
    cat.name AS category,
    ROUND(SUM(con.USD_pledged), 2) AS total_raised,
    SUM(con.backers) AS total_backers,
    COUNT(*) AS campaign_count
FROM condensed con
JOIN sub_category s ON con.sub_category_id = s.id
JOIN category cat ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_raised DESC
""" % {"condensed": VIEW_CONDENSED}

VIZ_GEOGRAPHIC = """
WITH condensed AS (%(condensed)s)
SELECT
    co.name AS country,
    COUNT(*) AS campaign_count,
    ROUND(SUM(con.USD_pledged), 2) AS total_pledged
FROM condensed con
JOIN country co ON co.id = con.country_id
WHERE con.outcome = 'successful'
GROUP BY country
ORDER BY total_pledged DESC
LIMIT 5
""" % {"condensed": VIEW_CONDENSED}

VIZ_DURATION_LINE = """
WITH condensed AS (%(condensed)s)
SELECT
    CAST(days AS INTEGER) AS duration,
    ROUND(AVG(USD_pledged), 2) AS avg_raised,
    COUNT(*) AS campaign_count
FROM condensed
WHERE days BETWEEN 1 AND 92
GROUP BY duration
ORDER BY duration
""" % {"condensed": VIEW_CONDENSED}

VIZ_EXEC_SUCCESS_STATS = """
WITH condensed AS (%(condensed)s)
SELECT
    ROUND(AVG(USD_goal), 0)    AS avg_success_goal,
    ROUND(AVG(USD_pledged), 0) AS avg_success_pledged,
    ROUND(AVG(backers), 0)     AS avg_backers
FROM condensed
WHERE outcome = 'successful'
""" % {"condensed": VIEW_CONDENSED}

VIZ_EXEC_TABLETOP_STATS = """
WITH condensed AS (%(condensed)s)
SELECT
    ROUND(AVG(USD_pledged), 0) AS avg_tabletop_pledged,
    ROUND(AVG(backers), 0)     AS avg_tabletop_backers
FROM condensed con
JOIN sub_category s ON con.sub_category_id = s.id
WHERE LOWER(s.name) LIKE '%%tabletop%%'
  AND con.outcome = 'successful'
""" % {"condensed": VIEW_CONDENSED}
