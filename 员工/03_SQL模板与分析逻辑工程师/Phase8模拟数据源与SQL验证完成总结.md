# Phase 8 模拟数据源与 SQL 验证完成总结

## 本轮交付

本轮按更新后的任务书收口，没有继续做 Docker 环境工程，重点交付了“可导入任意 SQL 平台的模拟数据包 + 配套说明 + 可参考 SQL”。

新增资产：

- `mock_data/user_orders.csv`
- `mock_data/user_events.csv`
- `mock_data/mysql/init.sql`
- `mock_data/postgresql/init.sql`
- `mock_data/reference_sql/trend_example.mysql.sql`
- `mock_data/reference_sql/compare_example.postgresql.sql`
- `mock_data/reference_sql/retention_example.mysql.sql`
- `docs/MOCK_DATA_GUIDE.md`
- `tests/test_mock_data_assets.py`

同时在 `README.md` 增加了 mock data 验证入口。

## 这批数据解决了什么

### 1. 趋势分析示例可验证

`user_orders` 已覆盖当前页面的 `trend` 示例字段与筛选条件：

- 表：`user_orders`
- 日期字段：`order_date`
- 指标字段：`amount`
- 筛选：`channel IN ('organic', 'ads')`

`2026-03-01 ~ 2026-03-31` 每天都提供 `organic` 和 `ads` 记录，生成的趋势 SQL 可以直接在外部数据库平台验证。

### 2. 同比示例可验证

同一张 `user_orders` 表中补齐了 `APAC` 在 `2025` 和 `2026` 的 `1-3 月` 数据，因此当前页面 `compare` 示例生成的 PostgreSQL 同比 SQL 可以直接校验 `previous_value`、`absolute_change` 和 `change_rate`。

### 3. 留存示例可验证

`user_events` 按当前页面示例补齐了：

- `user_id`
- `event_time`
- `platform`
- `1 / 3 / 7 / 14 / 30` 天回访

因此当前页面生成的 `retention curve` SQL 可以直接在 MySQL 或兼容平台验证。

## 配套说明

主说明文档已经整理到：

- `docs/MOCK_DATA_GUIDE.md`

文档重点说明了：

- 两张表的字段含义
- 如何通过 `init.sql` 或 CSV 导入外部平台
- 如何对应到页面当前三组示例参数
- 页面生成 SQL 后应该看到的实际结果字段名
- 参考 SQL 文件位置

## 验证与测试

本轮补了轻量资产测试 `tests/test_mock_data_assets.py`，覆盖：

- CSV 文件存在且字段名正确
- `user_orders.csv` 的日期范围、`organic/ads/APAC` 覆盖
- `user_events.csv` 的日期范围、`ios/android` 与 `1/3/7/14/30` 回访覆盖
- MySQL / PostgreSQL `init.sql` 与参考 SQL 文件存在且包含关键结构

建议项目经理或下一位同事按以下方式继续验收：

1. 在任意 MySQL 或 PostgreSQL 平台导入 `mock_data` 下的数据。
2. 在页面加载对应示例。
3. 生成 SQL 并粘贴到目标平台执行。
4. 对照 `docs/MOCK_DATA_GUIDE.md` 和 `mock_data/reference_sql/` 核验结果结构。

## 未扩范围项

本轮没有继续推进：

- Docker 启动脚本或容器化验证流程
- 真实数据库连接
- 页面执行 SQL 按钮
- 新的分析类型

这次交付刻意保持“小而全”，优先保证新手容易导入、容易看懂、容易验证。

## 下一步建议

下一位建议优先对接 `04_前端工程师_Streamlit` 或项目经理：

- 前端可在页面中补一个“示例数据验证说明”入口，直接跳转 `docs/MOCK_DATA_GUIDE.md`
- 项目经理可据此安排老板演示或跨平台验证
