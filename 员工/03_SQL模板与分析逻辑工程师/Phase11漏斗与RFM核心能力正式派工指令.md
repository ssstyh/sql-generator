# Phase 11 漏斗与 RFM 核心能力正式派工指令

你现在接手 `Phase 11 / 漏斗与 RFM 核心能力接入`。

先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [app.py](/E:/sql-generator/app.py)
- [core/generator.py](/E:/sql-generator/core/generator.py)
- [core/validator.py](/E:/sql-generator/core/validator.py)
- [templates/funnel.sql.j2](/E:/sql-generator/templates/funnel.sql.j2)
- [templates/rfm.sql.j2](/E:/sql-generator/templates/rfm.sql.j2)
- [员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力任务书.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力任务书.md)

本轮优先使用的 skills：

- `discover-database`
- `query-builder`

你的核心目标不是继续做演示版收口，而是把完整版本里缺失的两项核心分析能力真正落地：`漏斗分析` 与 `RFM 分析`。

本轮必须完成：

1. 实现漏斗分析真实 SQL 模板
2. 实现 RFM 分析真实 SQL 模板
3. 接好生成器与校验器链路
4. 补齐相关测试
5. 在你自己的文件夹下提交 `Phase11漏斗与RFM核心能力完成总结.md`

本轮不做：

- 真实数据库接入
- 大范围前端改版
- 擅自修改其他员工既有总结文件

验收以“漏斗与 RFM 是否已经具备真实可生成 SQL 的核心能力”为准。
