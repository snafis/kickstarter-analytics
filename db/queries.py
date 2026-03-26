# All SQL as named constants.
# Formatted following sqlstyle.guide — keywords right-aligned to form a
# consistent "river" of whitespace on the left side of each clause.

# ── Schema exploration ─────────────────────────────────────────────────────────

QC_ALL_OUTCOMES = """\
  SELECT outcome,
         COUNT(*) AS campaign_count
    FROM campaign
GROUP BY outcome
ORDER BY campaign_count DESC"""

QC_EXPLORE_CURRENCIES = """\
  SELECT cu.name    AS currency,
         COUNT(*)   AS campaign_count
    FROM campaign AS c
    JOIN currency AS cu
      ON c.currency_id = cu.id
GROUP BY cu.name
ORDER BY campaign_count DESC"""

QC_ALL_CATEGORIES = """\
  SELECT cat.name              AS category,
         COUNT(DISTINCT s.id)  AS subcategory_count,
         COUNT(c.id)           AS campaign_count
    FROM category AS cat
    JOIN sub_category AS s
      ON s.category_id = cat.id
    JOIN campaign AS c
      ON c.sub_category_id = s.id
GROUP BY cat.name
ORDER BY campaign_count DESC"""

QC_SAMPLE_CAMPAIGNS = """\
SELECT c.id,
       c.name,
       c.outcome,
       c.goal,
       c.pledged,
       c.backers,
       s.name   AS sub_category,
       cat.name AS category,
       co.name  AS country,
       cu.name  AS currency,
       c.launched,
       c.deadline
  FROM campaign AS c
  JOIN sub_category AS s
    ON c.sub_category_id = s.id
  JOIN category AS cat
    ON s.category_id = cat.id
  JOIN country AS co
    ON c.country_id = co.id
  JOIN currency AS cu
    ON c.currency_id = cu.id
 LIMIT 50"""

QC_COUNTRY_ANOMALY = """\
  SELECT co.name  AS country,
         COUNT(*) AS campaign_count
    FROM campaign AS c
    JOIN country AS co
      ON c.country_id = co.id
GROUP BY co.name
ORDER BY campaign_count DESC"""

# ── Data quality checks ────────────────────────────────────────────────────────

QC_ZERO_BACKERS_WITH_PLEDGED = """\
SELECT COUNT(*) AS anomalous_rows
  FROM campaign
 WHERE backers = 0
   AND pledged > 0"""

# ── Analysis queries (all use v_condensed view) ────────────────────────────────

Q1_OUTCOME_AVERAGES = """\
  SELECT outcome,
         ROUND(AVG(usd_goal), 2)    AS avg_goal_usd,
         ROUND(AVG(usd_pledged), 2) AS avg_pledged_usd,
         ROUND(AVG(backers), 0)     AS avg_backers,
         COUNT(*)                   AS campaign_count
    FROM v_condensed
GROUP BY outcome
ORDER BY outcome DESC"""

Q2_TOP_CATEGORIES_BACKERS = """\
  SELECT cat.name           AS category,
         SUM(c.backers)     AS total_backers,
         SUM(c.backers) / COUNT(*) AS avg_backers
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
    JOIN category AS cat
      ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_backers DESC
   LIMIT 3"""

Q2_BOTTOM_CATEGORIES_BACKERS = """\
  SELECT cat.name           AS category,
         SUM(c.backers)     AS total_backers,
         SUM(c.backers) / COUNT(*) AS avg_backers
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
    JOIN category AS cat
      ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_backers ASC
   LIMIT 3"""

Q2_TOP_SUBCATEGORIES_BACKERS = """\
  SELECT s.name             AS sub_category,
         SUM(c.backers)     AS total_backers,
         SUM(c.backers) / COUNT(*) AS avg_backers
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
GROUP BY s.name
ORDER BY total_backers DESC
   LIMIT 3"""

Q2_BOTTOM_SUBCATEGORIES_BACKERS = """\
  SELECT s.name             AS sub_category,
         SUM(c.backers)     AS total_backers,
         SUM(c.backers) / COUNT(*) AS avg_backers
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
GROUP BY s.name
ORDER BY total_backers ASC
   LIMIT 3"""

Q3_TOP_CATEGORIES_MONEY = """\
  SELECT cat.name                          AS category,
         ROUND(SUM(c.usd_pledged), 2)      AS total_raised,
         ROUND(SUM(c.usd_pledged) / COUNT(*), 2) AS avg_raised
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
    JOIN category AS cat
      ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_raised DESC
   LIMIT 3"""

Q3_BOTTOM_CATEGORIES_MONEY = """\
  SELECT cat.name                          AS category,
         ROUND(SUM(c.usd_pledged), 2)      AS total_raised,
         ROUND(SUM(c.usd_pledged) / COUNT(*), 2) AS avg_raised
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
    JOIN category AS cat
      ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_raised ASC
   LIMIT 3"""

Q3_TOP_SUBCATEGORIES_MONEY = """\
  SELECT s.name                            AS sub_category,
         ROUND(SUM(c.usd_pledged), 2)      AS total_raised,
         ROUND(SUM(c.usd_pledged) / COUNT(*), 2) AS avg_raised
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
GROUP BY s.name
ORDER BY total_raised DESC
   LIMIT 3"""

Q3_BOTTOM_SUBCATEGORIES_MONEY = """\
  SELECT s.name                            AS sub_category,
         ROUND(SUM(c.usd_pledged), 2)      AS total_raised,
         ROUND(SUM(c.usd_pledged) / COUNT(*), 2) AS avg_raised
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
GROUP BY s.name
ORDER BY total_raised ASC
   LIMIT 3"""

Q4_BEST_TABLETOP_GAME = """\
  SELECT camp.name,
         con.id,
         con.backers,
         ROUND(con.usd_pledged, 2)                   AS usd_pledged,
         ROUND(con.usd_goal, 2)                       AS usd_goal,
         ROUND(con.usd_pledged / con.backers, 2)      AS avg_pledge_per_backer
    FROM v_condensed AS con
    JOIN sub_category AS s
      ON con.sub_category_id = s.id
    JOIN campaign AS camp
      ON con.id = camp.id
   WHERE LOWER(s.name) LIKE '%tabletop%'
     AND con.outcome = 'successful'
ORDER BY con.usd_pledged DESC
   LIMIT 1"""

Q5_TOP_COUNTRIES = """\
  SELECT co.name          AS country,
         COUNT(*)         AS number_of_campaigns,
         ROUND(SUM(c.usd_pledged), 2)         AS total_pledged,
         ROUND(SUM(c.usd_pledged) / COUNT(*), 2) AS avg_pledged,
         SUM(c.backers)   AS total_backers
    FROM v_condensed AS c
    JOIN country AS co
      ON co.id = c.country_id
   WHERE c.outcome = 'successful'
GROUP BY country
ORDER BY total_pledged DESC
   LIMIT 3"""

Q6_DURATION_IMPACT = """\
  SELECT CAST(days AS INTEGER) AS duration,
         ROUND(AVG(usd_pledged), 2) AS avg_raised,
         COUNT(*)                   AS campaign_count
    FROM v_condensed
   WHERE days BETWEEN 1 AND 92
GROUP BY duration
ORDER BY duration"""

# ── Visualization data queries ─────────────────────────────────────────────────

VIZ_SCATTER_DATA = """\
SELECT ROUND(usd_goal, 2)    AS usd_goal,
       ROUND(usd_pledged, 2) AS usd_pledged,
       outcome
  FROM v_condensed
 WHERE usd_goal > 0
   AND usd_pledged >= 0"""

VIZ_GOAL_HISTOGRAM = """\
SELECT ROUND(usd_goal, 2) AS usd_goal,
       outcome
  FROM v_condensed
 WHERE usd_goal BETWEEN 1 AND 500000
 ORDER BY outcome"""

VIZ_CATEGORY_PERFORMANCE = """\
  SELECT cat.name                      AS category,
         ROUND(SUM(c.usd_pledged), 2)  AS total_raised,
         SUM(c.backers)                AS total_backers,
         COUNT(*)                      AS campaign_count
    FROM v_condensed AS c
    JOIN sub_category AS s
      ON c.sub_category_id = s.id
    JOIN category AS cat
      ON s.category_id = cat.id
GROUP BY cat.name
ORDER BY total_raised DESC"""

VIZ_GEOGRAPHIC = """\
  SELECT co.name          AS country,
         COUNT(*)         AS campaign_count,
         ROUND(SUM(c.usd_pledged), 2) AS total_pledged
    FROM v_condensed AS c
    JOIN country AS co
      ON co.id = c.country_id
   WHERE c.outcome = 'successful'
GROUP BY country
ORDER BY total_pledged DESC
   LIMIT 5"""

VIZ_DURATION_LINE = """\
  SELECT CAST(days AS INTEGER)      AS duration,
         ROUND(AVG(usd_pledged), 2) AS avg_raised,
         COUNT(*)                   AS campaign_count
    FROM v_condensed
   WHERE days BETWEEN 1 AND 92
GROUP BY duration
ORDER BY duration"""

VIZ_EXEC_SUCCESS_STATS = """\
SELECT ROUND(AVG(usd_goal), 0)    AS avg_success_goal,
       ROUND(AVG(usd_pledged), 0) AS avg_success_pledged,
       ROUND(AVG(backers), 0)     AS avg_backers
  FROM v_condensed
 WHERE outcome = 'successful'"""

VIZ_EXEC_TABLETOP_STATS = """\
SELECT ROUND(AVG(c.usd_pledged), 0) AS avg_tabletop_pledged,
       ROUND(AVG(c.backers), 0)     AS avg_tabletop_backers
  FROM v_condensed AS c
  JOIN sub_category AS s
    ON c.sub_category_id = s.id
 WHERE LOWER(s.name) LIKE '%tabletop%'
   AND c.outcome = 'successful'"""
