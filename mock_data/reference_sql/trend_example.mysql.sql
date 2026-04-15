/*
  分析主题: 趋势分析
  analysis_type: trend
  dialect: mysql
  generated_at: reference_snapshot
  说明: 输出 day 粒度趋势指标
  聚合方式: sum
  日期范围: 2026-03-01 ~ 2026-03-31
  筛选条件数: 1
*/
WITH source_data AS (
  SELECT
    DATE(order_date) AS period_start,
    amount AS metric_value_source
  FROM user_orders
  WHERE 1 = 1
    AND DATE(order_date) >= '2026-03-01'
    AND DATE(order_date) <= '2026-03-31'
    AND channel IN ('organic', 'ads')
),
base_series AS (
  SELECT
    period_start,
    SUM(metric_value_source) AS metric_value
  FROM source_data
  GROUP BY period_start
)
SELECT
  period_start,
  metric_value
FROM base_series
ORDER BY period_start;
