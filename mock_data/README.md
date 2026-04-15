# 模拟数据包说明

## 这包数据是给谁用的

这包数据用于验证当前页面已经开放的三类分析能力：

- 趋势分析
- 同比 / 环比分析
- 留存分析

它不是完整业务库，只是为了让你能在外部数据库工具或平台里导入后，直接验证页面示例 SQL。

## 包里有什么

- `user_orders.csv`
- `user_events.csv`
- `mysql/init.sql`
- `postgresql/init.sql`
- `reference_sql/trend_example.mysql.sql`
- `reference_sql/compare_example.postgresql.sql`
- `reference_sql/retention_example.mysql.sql`

## 两张表的字段

### `user_orders`

| 字段 | 含义 |
| --- | --- |
| `order_id` | 订单 ID |
| `user_id` | 用户 ID |
| `order_date` | 下单时间 |
| `amount` | 订单金额 |
| `channel` | 渠道 |
| `region` | 区域 |

这张表用来支撑：

- 趋势分析示例
- 同比 / 环比示例

### `user_events`

| 字段 | 含义 |
| --- | --- |
| `event_id` | 事件 ID |
| `user_id` | 用户 ID |
| `event_time` | 事件时间 |
| `platform` | 平台 |

这张表用来支撑：

- 留存分析示例

## 和页面示例怎么对齐

### 趋势分析示例

- 表名：`user_orders`
- 日期字段：`order_date`
- 指标字段：`amount`
- 筛选条件：`channel IN ('organic', 'ads')`

### 同比 / 环比示例

- 表名：`user_orders`
- 日期字段：`order_date`
- 指标字段：`amount`
- 筛选条件：`region = 'APAC'`

### 留存分析示例

- 表名：`user_events`
- 用户字段：`user_id`
- 日期字段：`event_time`
- 筛选条件：`platform IN ('ios', 'android')`

## 推荐怎么用

如果你已经有 MySQL 或 PostgreSQL：

1. 直接执行对应方言的 `init.sql`
2. 或者先导入 `csv`，再按字段名建表
3. 到页面里加载对应示例
4. 生成 SQL 后贴到你的数据库工具里执行

如果你只想先对照 SQL 长什么样，可以先看 `reference_sql/` 里的三份参考文件。
