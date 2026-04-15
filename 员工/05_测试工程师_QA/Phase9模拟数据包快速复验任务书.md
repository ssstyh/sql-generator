# Phase 9 模拟数据包快速复验任务书

## 你的身份

你是 `05_测试工程师_QA`，本轮负责对 Phase 8 新增的 mock data 数据包、说明文档和参考 SQL 做快速复验。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [docs/MOCK_DATA_GUIDE.md](/E:/sql-generator/docs/MOCK_DATA_GUIDE.md)
7. [app.py](/E:/sql-generator/app.py)
8. [员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证完成总结.md)

## 本轮必须优先使用的 skills

- `pytest-patterns`
- `discover-database`

## 本轮任务目标

确认这套模拟数据包是否真的足够让老板或新手在外部平台完成示例 SQL 验证，而不是只在文档层面看起来合理。

## 你这轮要完成什么

### 1. 复核 mock data 资产完整性

至少检查以下内容：

- `mock_data/user_orders.csv`
- `mock_data/user_events.csv`
- `mock_data/mysql/init.sql`
- `mock_data/postgresql/init.sql`
- `mock_data/reference_sql/`
- `docs/MOCK_DATA_GUIDE.md`
- `tests/test_mock_data_assets.py`

### 2. 复核示例参数与数据包一致性

重点确认当前 `app.py` 的三组 `EXAMPLES` 与数据包一致：

- `trend`
- `compare`
- `retention`

### 3. 重跑测试基线

至少重跑：

- `python -m pytest`

如果你认为有必要，也可以单独跑 mock data 资产测试并在总结中写清楚。

### 4. 做一轮快速可用性判断

优先判断：

- 文档是否足够让新手照着做
- 字段说明是否足够清楚
- 参考 SQL 是否和当前真实生成结果结构一致
- 这轮交付是否还存在阻塞老板验证的缺口

如果你本地有可用数据库环境，也可以额外做一条实际导入与执行验证；如果没有，也要在总结里明确写出限制，不要假装做过。

## 明确不要做什么

- 不要扩范围去修产品功能
- 不要擅自改 mock data 的业务设计
- 不要修改其他员工文件夹里的既有总结文件
- 不要把这轮复验膨胀成完整 E2E 项目

## 验收标准

- 你给出明确结论：`通过 / 有问题需返工`
- 若不通过，问题必须可定位、可复现、可交回 SQL 工程师修正
- 若通过，说明 mock data 数据包已具备老板演示与外部平台验证条件
- 你在自己的文件夹下提交 [Phase9模拟数据包快速复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase9模拟数据包快速复验完成总结.md)

## 完成后必须提交

请在你的文件夹下新增：

- `Phase9模拟数据包快速复验完成总结.md`

总结里至少写清楚：

- 你复核了哪些文件
- 你执行了哪些命令
- 你的结论是通过还是不通过
- 如有缺陷，缺陷点是什么
