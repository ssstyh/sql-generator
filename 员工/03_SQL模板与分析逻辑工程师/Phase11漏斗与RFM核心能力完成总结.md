# Phase 11 漏斗与 RFM 核心能力完成总结

## 本轮完成内容

本轮已把 `漏斗分析` 与 `RFM 分析` 从占位模板补齐为真实可生成 SQL 的核心能力，并接入现有的：

- `InputValidator`
- `SQLGenerator`
- `Jinja2 template`
- `SQLFormatter`

本轮没有做真实数据库接入，也没有推进前端大改版。

## 修改文件

核心代码：

- `core/generator.py`
- `core/validator.py`
- `templates/funnel.sql.j2`
- `templates/rfm.sql.j2`

测试：

- `tests/test_funnel.py`
- `tests/test_rfm.py`
- `tests/test_validator.py`

## 漏斗分析输入假设

本轮漏斗分析采用“单事件表 + 分步骤筛选条件”的最小可落地模型：

- 顶层必填：
  - `table_name`
  - `user_id_field`
  - `date_field`
  - `steps`
- 顶层可选：
  - `date_range`
  - `window_days`，默认 `7`
  - `filter_conditions`

`steps` 本轮固定为对象列表，每步至少包含：

- `step_name`

每步可选包含：

- `table_name`
- `user_id_field`
- `date_field`
- `filter_conditions`

实际落地逻辑：

- 第一步先取每个用户满足该步骤条件的最早事件时间
- 后续步骤必须在前一步之后发生，且落在 `window_days` 转化窗口内
- 输出字段为：
  - `step_order`
  - `step_name`
  - `user_count`
  - `conversion_rate`
  - `overall_conversion_rate`

## RFM 输入假设

本轮 RFM 采用“订单事实表 + 用户级聚合 + NTILE 分箱”的最小可落地模型：

- 必填：
  - `table_name`
  - `user_id_field`
  - `date_field`
  - `amount_field`
- 可选：
  - `analysis_date`，默认当天
  - `r_bins`，默认 `5`
  - `f_bins`，默认 `5`
  - `m_bins`，默认 `5`
  - `filter_conditions`

实际落地逻辑：

- `recency_days`：`analysis_date - 最近一次下单日`
- `frequency_value`：订单次数
- `monetary_value`：金额求和
- 使用 `NTILE` 做 R/F/M 分箱
- 输出字段为：
  - `user_id`
  - `analysis_date`
  - `recency_days`
  - `frequency_value`
  - `monetary_value`
  - `r_score`
  - `f_score`
  - `m_score`
  - `rfm_score`
  - `segment_label`

本轮 `segment_label` 采用 8 类 CASE WHEN 标签：

- `champions`
- `loyal_customers`
- `big_spenders`
- `potential_loyalists`
- `at_risk_vips`
- `needs_attention`
- `one_time_big_spenders`
- `hibernating`

## 校验器补齐内容

新增或增强的校验包括：

- 漏斗 `steps` 至少 2 步
- 每个 step 必须是对象且有非空 `step_name`
- 漏斗 step 名称必须唯一
- `window_days` 必须为正整数，默认 `7`
- `analysis_date` 默认当天，且必须符合 `YYYY-MM-DD`
- `r_bins / f_bins / m_bins` 默认 `5`，且必须 `>= 2`
- 继续复用并扩展现有 `filter_conditions` 规则到漏斗 step 级条件

## 本地验证方式

我本地使用以下方式验证：

1. 直接通过 `SQLGenerator.generate()` 生成漏斗 / RFM SQL
2. 查看 MySQL 与 PostgreSQL 双方言输出片段是否符合预期
3. 跑新增测试：
   - `tests/test_funnel.py`
   - `tests/test_rfm.py`
   - `tests/test_validator.py`
4. 跑全量回归：

```bash
python -m pytest
```

结果：

- `46 passed`

## 当前仍未完成的后续工作

本轮已完成核心 SQL 能力，但后续仍有这些工作：

- 前端尚未开放漏斗 / RFM 的真实表单
- `app.py` 里漏斗 / RFM 仍处于未开放提示状态
- 还没有针对漏斗 / RFM 补 mock data 验证包
- QA 后续仍需要做一轮针对漏斗 / RFM 的完整功能复验

## 建议下一棒

下一位建议优先交给：

- `04_前端工程师_Streamlit`

原因：

- 生成器、校验器、模板和测试已经齐了
- 前端现在可以基于本轮输入假设把漏斗 / RFM 的参数表单接出来
- 前端接入后再由 QA 做完整回归会更顺
