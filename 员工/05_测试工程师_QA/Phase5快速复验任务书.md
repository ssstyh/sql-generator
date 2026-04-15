# Phase 5 快速复验任务书：测试工程师（QA）

## 你的角色

你本轮接手的是收口前的快速复验任务。重点不是重新做一轮大而全的测试，而是基于最新的 P1 修复结果和最新的最小 CI，快速判断当前版本是否已经可以进入部署与展示收口阶段。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [.github/workflows/pytest.yml](/E:/sql-generator/.github/workflows/pytest.yml)
7. [员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md)
8. [员工/02_技术负责人_后端架构师/最小CI接入完成总结.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/最小CI接入完成总结.md)
9. [员工/05_测试工程师_QA/Day7完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Day7完成总结.md)
10. [员工/05_测试工程师_QA/岗位职责说明.md](/E:/sql-generator/员工/05_测试工程师_QA/岗位职责说明.md)
11. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)

## 你要优先使用的 Skills

- `pytest-patterns`
- `github-actions`

## 本轮任务目标

在当前最小 CI 已接入的前提下，对最新版本做一轮高信号、低冗余的快速复验，输出“通过 / 不通过”结论，并明确下一步应如何收口。

## 具体任务

### 任务 1：重跑当前基础验证

请先执行并记录：

- `python -c "import app; print('app import ok')"`
- `python -m pytest`

### 任务 2：复核最小 CI 口径

请检查 [.github/workflows/pytest.yml](/E:/sql-generator/.github/workflows/pytest.yml) 是否与当前仓库状态一致，重点确认：

- 触发条件是否为 `push` / `pull_request`
- Python 版本是否为 `3.11`
- 是否先做 `app import` 冒烟检查
- 是否执行 `python -m pytest`

### 任务 3：快速复验两个已修复的 P1 场景

请重点确认：

- 成功生成后，历史记录是否即时显示
- 新一轮生成失败后，旧成功提示和旧 SQL 是否已清空

### 任务 4：快速复验主流程

请围绕当前三类已开放分析能力确认主流程是否仍稳定：

- 趋势分析
- 对比分析（同比 / 环比）
- 留存分析
- 示例加载
- 历史回看与清空
- 结果展示、复制、下载
- 漏斗 / RFM 未开放时的提示是否清晰

### 任务 5：必要时补充测试

如果你判断当前自动化覆盖仍有明显空白，可以在 `tests/` 下补最小必要回归测试；如果没有必要，也请在总结里明确写出“不需要补测”的理由。

### 任务 6：提交完成总结

你完成后必须在自己的文件夹下生成：

- [员工/05_测试工程师_QA/Phase5快速复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase5快速复验完成总结.md)

## 完成总结必须包含

- 你阅读了哪些文件
- 你执行了哪些命令及结果
- 你复验了哪些核心场景
- 当前结论是“通过”还是“未通过”
- 如果未通过，阻塞项是什么
- 你建议下一步交给谁以及为什么

## 验收标准

- QA 给出明确“通过 / 不通过”结论
- 两个 P1 修复点被再次确认
- 当前主流程复验结论清晰
- 如有问题，缺陷可复现、可跟踪
- `Phase5快速复验完成总结.md` 已提交
