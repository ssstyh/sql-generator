# Phase 8 模拟数据包与外部平台验证正式派工指令

你现在接手 `Phase 8 / 模拟数据包与外部平台验证增强`。

先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [docs/USER_GUIDE.md](/E:/sql-generator/docs/USER_GUIDE.md)
- [app.py](/E:/sql-generator/app.py)
- [员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证任务书.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase8模拟数据源与SQL验证任务书.md)

本轮优先使用的 skills：

- `discover-database`
- `query-builder`

你的核心目标不是新增业务分析类型，而是把当前三类已开放能力补齐成“拿着模拟数据包就能在别的平台验证”的状态。

本轮必须完成：

1. 为 `user_orders` 和 `user_events` 设计并落地模拟数据源
2. 提供字段说明与至少一份可参考的初始化 SQL
3. 让当前示例参数生成出的 SQL 能在外部平台对着模拟数据跑验证
4. 输出新手可执行的验证说明
5. 如有必要补测试，但不得破坏现有测试基线
6. 在你自己的文件夹下提交 `Phase8模拟数据源与SQL验证完成总结.md`

本轮不做：

- 漏斗分析
- RFM
- 真实数据库接入
- 大范围前端改版
- 把主交付做成 Docker 环境工程

验收以“老板或新手能否把模拟数据导入到自己熟悉的平台，然后用当前示例 SQL 验证结果”为准。
