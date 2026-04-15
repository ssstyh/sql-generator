# 正式派工指令

## 指令对象

`05_测试工程师_QA`

## 派工背景

前端工程师已完成两个 P1 页面缺陷修复，技术负责人也已补上最小 GitHub Actions `pytest` CI。当前本地基线为：

- `python -c "import app; print('app import ok')"` -> passed
- `python -m pytest` -> `36 passed`

你本轮的职责，是基于这条最新基线做一轮快速复验，给项目一个明确的阶段性结论。

## 执行要求

开始前请先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [.github/workflows/pytest.yml](/E:/sql-generator/.github/workflows/pytest.yml)
- [员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md)
- [员工/02_技术负责人_后端架构师/最小CI接入完成总结.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/最小CI接入完成总结.md)
- [员工/05_测试工程师_QA/Day7完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Day7完成总结.md)

本轮优先使用的 skills：

- `pytest-patterns`
- `github-actions`

## 本轮正式任务

1. 重跑 `app import` 与 `pytest`
2. 复核最小 CI 工作流口径
3. 快速复验两个已修复的 P1 场景
4. 快速复验趋势 / 对比 / 留存主流程
5. 输出明确“通过 / 不通过”结论

## 明确禁止事项

- 不要把这轮快速复验重新做成一轮大而全的全面测试
- 不要模糊输出“看起来没问题”这类无法交接的结论
- 不要跳过已修复 P1 场景
- 不要改动与你任务无关的员工文件

## 交付清单

你完成后必须交付：

- 必要时更新的最小测试内容
- 复验结论
- 你个人文件夹下的 `Phase5快速复验完成总结.md`

## 完成总结硬性要求

你必须像之前一样，在自己的文件夹下提交完成总结文件，文件名固定为：

- `Phase5快速复验完成总结.md`

没有这份总结，项目经理视为本轮交付不完整。

## 验收口径

- QA 给出清晰阶段结论
- 结论能指导下一位执行人
- 若有阻塞项，描述清楚、可复现、可跟踪
- 若无阻塞项，项目可切入部署与展示收口
