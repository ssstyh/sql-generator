# Mock Data Guide

这轮 Phase 8 的交付重点不是环境工程，而是让你把示例数据导入任意 SQL 平台后，直接验证页面当前会生成的示例 SQL。

## 交付内容

- `mock_data/user_orders.csv`
- `mock_data/user_events.csv`
- `mock_data/mysql/init.sql`
- `mock_data/postgresql/init.sql`
- `mock_data/reference_sql/trend_example.mysql.sql`
- `mock_data/reference_sql/compare_example.postgresql.sql`
- `mock_data/reference_sql/retention_example.mysql.sql`

## 两张模拟表

### `user_orders`

字段如下：

| 字段 | 类型参考 | 用途 |
| --- | --- | --- |
| `order_id` | 整数 | 订单主键 |
| `user_id` | 字符串 | 用户标识 |
| `order_date` | 日期时间 | 趋势与同比/环比的时间字段 |
| `amount` | 数值 | 示例里的指标字段 |
| `channel` | 字符串 | 趋势示例筛选字段 |
| `region` | 字符串 | 对比示例筛选字段 |

这张表专门对齐当前页面里的两个示例：

- `trend` 示例：`user_orders / order_date / amount / channel IN ('organic', 'ads')`
- `compare` 示例：`user_orders / order_date / amount / region = 'APAC'`

数据特征：

- 覆盖 `2025-01-01` 到 `2026-03-31`
- `2026-03-01 ~ 2026-03-31` 每天都有 `organic` 和 `ads`
- `2025` 与 `2026` 的 `1-3 月` 都有 `APAC`
- 同时保留少量 `email`、`referral`、非 `APAC` 记录，方便验证筛选条件是否真的生效

### `user_events`

字段如下：

| 字段 | 类型参考 | 用途 |
| --- | --- | --- |
| `event_id` | 整数 | 事件主键 |
| `user_id` | 字符串 | 留存分析用户标识 |
| `event_time` | 日期时间 | 留存分析时间字段 |
| `platform` | 字符串 | 留存示例筛选字段 |

这张表对齐当前页面里的 `retention` 示例：

- `user_events / user_id / event_time / platform IN ('ios', 'android')`

数据特征：

- 覆盖 `2026-02-01` 到 `2026-03-31`
- 包含 `ios` 与 `android` cohort 用户
- 明确覆盖 `1 / 3 / 7 / 14 / 30` 天回访
- 同时保留少量 `web`、`miniapp` 记录，方便验证平台筛选

## 推荐导入方式

如果你已经有 MySQL 或 PostgreSQL，优先直接执行对应的 `init.sql`：

- MySQL: `mock_data/mysql/init.sql`
- PostgreSQL: `mock_data/postgresql/init.sql`

如果你在 Navicat、DBeaver、DataGrip、Supabase、Cloud SQL 控制台等平台里操作，也可以直接：

1. 新建两张表，字段名保持与 CSV 一致。
2. 将 `mock_data/user_orders.csv` 导入 `user_orders`。
3. 将 `mock_data/user_events.csv` 导入 `user_events`。

只要字段名一致，页面生成的示例 SQL 就可以直接复用。

## 如何验证页面示例 SQL

### 1. 趋势分析

页面示例参数：

- 分析类型：`trend`
- 方言：`mysql`
- 表名：`user_orders`
- 日期字段：`order_date`
- 指标字段：`amount`
- 聚合：`sum`
- 粒度：`day`
- 日期范围：`2026-03-01 ~ 2026-03-31`
- 筛选：`channel IN ('organic', 'ads')`

执行后应看到的结果结构，以当前真实生成 SQL 为准：

- `period_start`
- `metric_value`

这份 mock data 下，结果应满足：

- `2026-03` 有 31 个日粒度结果
- `period_start` 从 `2026-03-01` 排到 `2026-03-31`
- 不会把 `email` 或 `referral` 的记录算进去

参考 SQL：

- [mock_data/reference_sql/trend_example.mysql.sql](/E:/sql-generator/mock_data/reference_sql/trend_example.mysql.sql)

### 2. 同比 / 环比分析

页面示例参数：

- 分析类型：`compare`
- 方言：`postgresql`
- 表名：`user_orders`
- 日期字段：`order_date`
- 指标字段：`amount`
- 聚合：`sum`
- 粒度：`month`
- 对比类型：`yoy`
- 日期范围：`2025-01-01 ~ 2026-03-31`
- 筛选：`region = 'APAC'`

执行后应看到的结果结构，以当前真实生成 SQL 为准：

- `period_start`
- `current_value`
- `previous_value`
- `absolute_change`
- `change_rate`

这份 mock data 下，结果应满足：

- `2026-01`、`2026-02`、`2026-03` 会对上 `2025` 同月数据
- 上面三个月的 `previous_value` 应为非空
- 非 `APAC` 数据不会进入结果

参考 SQL：

- [mock_data/reference_sql/compare_example.postgresql.sql](/E:/sql-generator/mock_data/reference_sql/compare_example.postgresql.sql)

### 3. 留存分析

页面示例参数：

- 分析类型：`retention`
- 方言：`mysql`
- 表名：`user_events`
- 用户字段：`user_id`
- 日期字段：`event_time`
- 留存天数：`[1, 3, 7, 14, 30]`
- 留存模式：`curve`
- 活动范围：`2026-02-01 ~ 2026-03-31`
- 筛选：`platform IN ('ios', 'android')`

执行后应看到的结果结构，以当前真实生成 SQL 为准：

- `cohort_date`
- `retention_day`
- `cohort_size`
- `retained_users`
- `retention_rate`

这份 mock data 下，结果应满足：

- `retention_day` 会出现 `1`、`3`、`7`、`14`、`30`
- `web` 和 `miniapp` 不会进入 cohort
- 至少能看到 `2026-02-01`、`2026-02-10`、`2026-03-01` 这几组 cohort

参考 SQL：

- [mock_data/reference_sql/retention_example.mysql.sql](/E:/sql-generator/mock_data/reference_sql/retention_example.mysql.sql)

## 建议使用顺序

1. 先导入 `init.sql` 或 CSV。
2. 打开页面，点击对应示例。
3. 生成 SQL。
4. 把页面生成 SQL 复制到你的数据库平台执行。
5. 如果想先对照结构，再查看 `mock_data/reference_sql/` 下的参考 SQL。

## 说明

- 这批数据是“小而全”的验证包，不是完整业务库。
- 重点是让页面当前三组示例参数有可验证的落地数据。
- 如果后续页面示例参数变化，需要同步更新这批 mock data 和参考 SQL。
