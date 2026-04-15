/*
  分析主题: 同比/环比分析
  analysis_type: compare
  dialect: postgresql
  generated_at: reference_snapshot
  说明: 输出 同比对比结果
  时间粒度: month
  聚合方式: sum
  日期范围: 2025-01-01 ~ 2026-03-31
  筛选条件数: 1
*/
WITH base_series AS (
  SELECT
    period_start,
    SUM(metric_value_source) AS metric_value
  FROM (
    SELECT
      DATE_TRUNC('month', order_date)::date AS period_start,
      amount AS metric_value_source
    FROM user_orders
    WHERE 1 = 1
      AND (order_date)::date >= '2025-01-01'
      AND (order_date)::date <= '2026-03-31'
      AND region = 'APAC'
  ) source_data
  GROUP BY period_start
)
SELECT
  curr.period_start,
  curr.metric_value AS current_value,
  prev.metric_value AS previous_value,
  curr.metric_value - prev.metric_value AS absolute_change,
  ROUND((curr.metric_value - prev.metric_value) * 1.0 / NULLIF(prev.metric_value, 0), 4) AS change_rate
FROM base_series curr
LEFT JOIN base_series prev
  ON curr.period_start = (prev.period_start + INTERVAL '1 year')::date
ORDER BY period_start;
