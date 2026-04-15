# 正式派工指令

## 指令对象

`02_技术负责人_后端架构师`

## 派工背景

前端工程师已完成 QA 提出的两个 P1 页面缺陷修复，并通过当前本地验证：

- `python -m pytest` -> `36 passed`
- `python -c "import app; print('app import ok')"` -> passed

当前仓库尚未接入 `.github/workflows/`，因此你本轮的职责是补上最小 GitHub Actions `pytest` CI，作为后续 QA 快速复验和最终演示前的自动化门禁。

## 执行要求

开始前请先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [员工/05_测试工程师_QA/Day7完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Day7完成总结.md)
- [员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md)
- [员工/02_技术负责人_后端架构师/岗位职责说明.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/岗位职责说明.md)

本轮优先使用的 skills：

- `github-actions`
- `system-architecture`

## 本轮正式任务

1. 在仓库中新增最小 GitHub Actions `pytest` 工作流
2. 让工作流在 `push` 和 `pull_request` 时触发
3. 让工作流安装依赖并执行 `python -m pytest`
4. 视稳定性决定是否加入 `app import` 冒烟检查
5. 保持业务代码范围不扩张

## 明确禁止事项

- 不新增漏斗、RFM 或其他业务功能
- 不做大范围目录重构
- 不把本轮工作扩展成完整部署流水线
- 不改动与你任务无关的员工文件

## 交付清单

你完成后必须交付：

- 最小 GitHub Actions 工作流文件
- 必要的最小同步说明
- 你个人文件夹下的 `最小CI接入完成总结.md`

## 完成总结硬性要求

你必须像前端工程师一样，在自己的文件夹下生成完成总结文件，文件名固定为：

- `最小CI接入完成总结.md`

没有这份总结，项目经理视为本轮交付不完整。

## 验收口径

- `.github/workflows/` 已存在最小测试工作流
- 工作流触发条件正确
- 工作流步骤清晰且可维护
- 当前本地测试结果没有退化
- 完成总结已提交

## 交付后的下一步

你交付后，项目经理将安排 QA 做快速复验；若 CI 和复验都通过，项目会继续进入功能收口与部署准备阶段。
