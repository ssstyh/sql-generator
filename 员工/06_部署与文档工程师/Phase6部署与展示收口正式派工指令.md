# 正式派工指令

## 指令对象

`06_部署与文档工程师`

## 派工背景

QA 已完成 Phase 5 快速复验，并明确给出“通过”结论。当前仓库状态为：

- `python -c "import app; print('app import ok')"` -> passed
- `python -m pytest` -> `36 passed`
- `python -m pytest tests/test_app_ui_regression.py -q` -> `7 passed`
- 最小 GitHub Actions `pytest` CI 已接入

因此你本轮的职责，是把当前版本整理成适合部署、展示和对外说明的状态。

## 执行要求

开始前请先阅读：

- [plan.md](/E:/sql-generator/plan.md)
- [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- [SESSION.md](/E:/sql-generator/SESSION.md)
- [README.md](/E:/sql-generator/README.md)
- [architecture.md](/E:/sql-generator/architecture.md)
- [.github/workflows/pytest.yml](/E:/sql-generator/.github/workflows/pytest.yml)
- [员工/05_测试工程师_QA/Phase5快速复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase5快速复验完成总结.md)
- [员工/06_部署与文档工程师/岗位职责说明.md](/E:/sql-generator/员工/06_部署与文档工程师/岗位职责说明.md)

本轮优先使用的 skills：

- `deployment-pipeline`
- `readme`

## 本轮正式任务

1. 收口 `README.md`
2. 补最小部署配置与部署说明
3. 补演示材料说明
4. 视情况补 `LICENSE`
5. 输出明确、可交接的完成总结

## 明确禁止事项

- 不新增业务功能
- 不修改核心 SQL 逻辑
- 不重新设计页面主流程
- 不把未完成的漏斗 / RFM / 真正线上部署结果写成“已完成”
- 不改动与你任务无关的员工文件

## 交付清单

你完成后必须交付：

- 最小部署与展示材料
- README 收口版本
- 你个人文件夹下的 `Phase6部署与展示收口完成总结.md`

## 完成总结硬性要求

你必须像之前一样，在自己的文件夹下提交完成总结文件，文件名固定为：

- `Phase6部署与展示收口完成总结.md`

没有这份总结，项目经理视为本轮交付不完整。

## 验收口径

- 文档口径真实、清晰、可对外交付
- 部署入口与说明具备可执行性
- 当前项目能力边界表达准确
- 下一步演示或收尾负责人可以直接接棒
