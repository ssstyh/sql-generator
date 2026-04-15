/*
  分析主题: 留存分析
  analysis_type: retention
  dialect: mysql
  generated_at: reference_snapshot
  说明: cohort 当天首次活跃，N 天后当天再次活跃即记为留存
  输出模式: curve
  留存天数: 1, 3, 7, 14, 30
  活跃过滤范围: 2026-02-01 ~ 2026-03-31
  筛选条件数: 1
*/
WITH filtered_events AS (
  SELECT DISTINCT
    user_id AS user_id,
    DATE(event_time) AS activity_date
  FROM user_events
  WHERE 1 = 1
    AND DATE(event_time) >= '2026-02-01'
    AND DATE(event_time) <= '2026-03-31'
    AND platform IN ('ios', 'android')
),
first_activity AS (
  SELECT
    user_id,
    MIN(activity_date) AS cohort_date
  FROM filtered_events
  GROUP BY user_id
),
cohort_retention AS (
  SELECT
    fa.cohort_date,
    fa.user_id,
    MAX(CASE WHEN fe.activity_date = DATE_ADD(fa.cohort_date, INTERVAL 1 DAY) THEN 1 ELSE 0 END) AS day_1_retained,
    MAX(CASE WHEN fe.activity_date = DATE_ADD(fa.cohort_date, INTERVAL 3 DAY) THEN 1 ELSE 0 END) AS day_3_retained,
    MAX(CASE WHEN fe.activity_date = DATE_ADD(fa.cohort_date, INTERVAL 7 DAY) THEN 1 ELSE 0 END) AS day_7_retained,
    MAX(CASE WHEN fe.activity_date = DATE_ADD(fa.cohort_date, INTERVAL 14 DAY) THEN 1 ELSE 0 END) AS day_14_retained,
    MAX(CASE WHEN fe.activity_date = DATE_ADD(fa.cohort_date, INTERVAL 30 DAY) THEN 1 ELSE 0 END) AS day_30_retained
  FROM first_activity fa
  LEFT JOIN filtered_events fe
    ON fe.user_id = fa.user_id
   AND fe.activity_date >= fa.cohort_date
   AND fe.activity_date <= DATE_ADD(fa.cohort_date, INTERVAL 30 DAY)
  GROUP BY fa.cohort_date, fa.user_id
),
cohort_summary AS (
  SELECT
    cohort_date,
    COUNT(*) AS cohort_size,
    SUM(day_1_retained) AS day_1_users,
    ROUND(SUM(day_1_retained) * 1.0 / NULLIF(COUNT(*), 0), 4) AS day_1_rate,
    SUM(day_3_retained) AS day_3_users,
    ROUND(SUM(day_3_retained) * 1.0 / NULLIF(COUNT(*), 0), 4) AS day_3_rate,
    SUM(day_7_retained) AS day_7_users,
    ROUND(SUM(day_7_retained) * 1.0 / NULLIF(COUNT(*), 0), 4) AS day_7_rate,
    SUM(day_14_retained) AS day_14_users,
    ROUND(SUM(day_14_retained) * 1.0 / NULLIF(COUNT(*), 0), 4) AS day_14_rate,
    SUM(day_30_retained) AS day_30_users,
    ROUND(SUM(day_30_retained) * 1.0 / NULLIF(COUNT(*), 0), 4) AS day_30_rate
  FROM cohort_retention
  GROUP BY cohort_date
)
SELECT
  cohort_date,
  retention_day,
  cohort_size,
  retained_users,
  retention_rate
FROM (
  SELECT cohort_date, 1 AS retention_day, cohort_size, day_1_users AS retained_users, day_1_rate AS retention_rate FROM cohort_summary
  UNION ALL
  SELECT cohort_date, 3 AS retention_day, cohort_size, day_3_users AS retained_users, day_3_rate AS retention_rate FROM cohort_summary
  UNION ALL
  SELECT cohort_date, 7 AS retention_day, cohort_size, day_7_users AS retained_users, day_7_rate AS retention_rate FROM cohort_summary
  UNION ALL
  SELECT cohort_date, 14 AS retention_day, cohort_size, day_14_users AS retained_users, day_14_rate AS retention_rate FROM cohort_summary
  UNION ALL
  SELECT cohort_date, 30 AS retention_day, cohort_size, day_30_users AS retained_users, day_30_rate AS retention_rate FROM cohort_summary
) curve_points
ORDER BY cohort_date, retention_day;
