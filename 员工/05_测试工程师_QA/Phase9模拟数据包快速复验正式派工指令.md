# Phase 9 模拟数据包快速复验正式派工指令

你现在接手 `Phase 9 / 模拟数据包快速复验`。

先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [docs/MOCK_DATA_GUIDE.md](/E:/sql-generator/docs/MOCK_DATA_GUIDE.md)
- [app.py](/E:/sql-generator/app.py)
- [员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证完成总结.md)
- [员工/05_测试工程师_QA/Phase9模拟数据包快速复验任务书.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase9模拟数据包快速复验任务书.md)

本轮优先使用的 skills：

- `pytest-patterns`
- `discover-database`

你的核心目标不是新增测试体系，而是快速确认 Phase 8 交付的 mock data 数据包是否真的可用于老板演示和外部平台验证。

本轮必须完成：

1. 复核 mock data 资产和说明文档
2. 复核当前三组示例参数与 mock data 的一致性
3. 重跑 `python -m pytest`
4. 给出明确的通过 / 不通过结论
5. 在你自己的文件夹下提交 `Phase9模拟数据包快速复验完成总结.md`

本轮不做：

- 新增分析类型
- 大规模重构测试体系
- 擅自修改其他员工的既有总结文件

验收以“这套 mock data 是否已经足够让老板或新手做外部平台验证”为准。
