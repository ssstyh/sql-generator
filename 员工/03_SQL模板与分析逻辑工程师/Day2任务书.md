# Day 2 任务书：SQL 模板与分析逻辑工程师

## 你的角色
你是本项目 Day 2 的关键执行人，负责把当前的“骨架态项目”推进成“具备第一批真实 SQL 产出的可用工具”。

你的工作重点不是页面，也不是部署，而是确保趋势分析、同比环比和留存分析的 SQL 逻辑正确、结构清晰、便于后续前端接入和 QA 验证。

## 先看哪些文件
开始前请按顺序阅读以下文件：

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [architecture.md](/E:/sql-generator/architecture.md)
5. [员工/02_技术负责人_后端架构师/Day1完成总结.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/Day1完成总结.md)
6. [员工/03_SQL模板与分析逻辑工程师/岗位职责说明.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/岗位职责说明.md)
7. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)
8. [项目概述.md](/E:/sql-generator/项目概述.md)

## 你要优先使用的 skills
- `discover-database`
  用途：先统一字段语义、时间口径、MySQL / PostgreSQL 差异和统计逻辑假设。
- `query-builder`
  用途：把趋势、同比环比、留存这些分析需求转成可执行 SQL 与模板结构。

## 你的 Day 2 具体任务

### 任务 1：实现趋势分析 SQL
请完成以下 3 类 SQL：
- 基础趋势 SQL
- 同比对比 SQL
- 环比对比 SQL

输入参数至少支持：
- `table_name`
- `date_field`
- `metric_field`
- `aggregation`
- `granularity`
- `user_id_field`（必要时）
- `filter_conditions`（可选）
- `date_range`（可选）
- `dialect`

对应修改位置：
- [templates/trend.sql.j2](/E:/sql-generator/templates/trend.sql.j2)
- [templates/compare.sql.j2](/E:/sql-generator/templates/compare.sql.j2)
- [core/generator.py](/E:/sql-generator/core/generator.py)
- [core/validator.py](/E:/sql-generator/core/validator.py)

### 任务 2：实现留存分析 SQL
请完成以下 2 类 SQL：
- 经典 N 日留存表
- 留存曲线数据 SQL

输入参数至少支持：
- `table_name`
- `user_id_field`
- `date_field`
- `retention_days`
- `start_date`
- `end_date`
- `filter_conditions`
- `dialect`

对应修改位置：
- [templates/retention.sql.j2](/E:/sql-generator/templates/retention.sql.j2)
- [core/generator.py](/E:/sql-generator/core/generator.py)
- [core/validator.py](/E:/sql-generator/core/validator.py)

### 任务 3：补齐业务校验
请在现有校验器基础上继续补齐：
- 聚合方式合法性
- 时间粒度合法性
- 留存天数列表合法性
- 可选筛选条件的基本结构约束
- 关键参数缺失时报错信息

### 任务 4：补齐 Day 2 测试
请新增并完善：
- `tests/test_trend.py`
- `tests/test_retention.py`

至少覆盖：
- MySQL / PostgreSQL 两种方言
- 趋势分析日/周/月粒度
- 同比与环比输出结构
- 留存 1/3/7/14/30 天场景
- 必填参数缺失与非法参数场景

### 任务 5：提交完成总结
任务完成后，你必须在自己的文件夹下生成：
- [员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md)

完成总结至少要包含：
- 本次完成了哪些文件
- 实现了哪些 SQL 能力
- 如何验证
- 当前未做内容
- 推荐下一个对接人是谁以及原因

## 你交付时必须满足的验收标准
- 趋势分析、同比环比、留存分析可以生成真实 SQL
- SQL 顶部带有清晰注释头，便于理解和演示
- 支持 `mysql` / `postgresql`
- `tests/test_trend.py` 与 `tests/test_retention.py` 可以通过
- 不要绕过 `SQLGenerator`，模板调用仍然走统一入口

## 你现在不要做的事
- 不要提前实现 Day 4 的漏斗和 RFM
- 不要把页面交互逻辑写进 SQL 模板层
- 不要绕过 `core/validator.py` 在模板里偷偷承担校验职责
- 不要为未来需求过早引入复杂抽象

## 项目经理对你的交接说明
技术负责人已经把骨架、入口、模板装载方式和模块边界准备好了。你现在最重要的是把第一批真实 SQL 产出来，而且要做到“能跑、能讲、能测”。尤其是留存逻辑，这是项目里最容易被 review 的高价值部分，必须写得清楚、稳妥、可解释。

## 老板可以直接这样对你说
请你接手 Day 2。先阅读 `plan.md`、`docs/ROADMAP.md`、`SESSION.md`、`architecture.md` 和技术负责人的完成总结，再优先使用 `discover-database` 与 `query-builder` 两个 skill。你的核心任务是实现趋势分析、同比环比和留存分析的真实 SQL 模板，补齐相应校验和测试，并在完成后在你的文件夹下提交 `Day2完成总结.md`，方便项目经理继续推进下一阶段。
