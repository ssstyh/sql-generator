# Phase 13 完整版本功能复验任务书

## 你的身份

你是 `05_测试工程师_QA`，本轮负责对完整版本新增的 `漏斗分析` 与 `RFM 分析` 页面能力做快速但系统化的功能复验。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [app.py](/E:/sql-generator/app.py)
7. [tests/test_app_ui_regression.py](/E:/sql-generator/tests/test_app_ui_regression.py)
8. [员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力完成总结.md)
9. [员工/04_前端工程师_Streamlit/Phase12前端开放漏斗与RFM完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/Phase12前端开放漏斗与RFM完成总结.md)

## 本轮必须优先使用的 skills

- `pytest-patterns`
- `debugging-streamlit`

## 本轮任务目标

确认漏斗分析与 RFM 分析是否已经从“后端已支持 + 页面已开放”推进到“完整版本可用且无明显阻塞缺陷”的状态。

## 你这轮要完成什么

### 1. 重跑完整测试基线

至少执行：

- `python -m pytest`

### 2. 重点复验漏斗与 RFM 页面链路

至少确认：

- funnel 页面可切换、可填写参数、可生成 SQL
- rfm 页面可切换、可填写参数、可生成 SQL
- 结果区、参数摘要、历史记录不回退
- 原有趋势 / 对比 / 留存链路未被新改动破坏

### 3. 评估是否存在阻塞完整版本验收的问题

重点留意：

- 参数映射是否和后端输入模型一致
- 页面是否存在明显难以理解或难以操作的问题
- 是否存在生成失败、状态错乱或结果展示缺失

如果你发现问题，请按严重程度写清楚并给出可复现路径。

## 明确不要做什么

- 不要顺手改产品代码
- 不要擅自扩到真实数据库连接或平台内执行层验证
- 不要修改其他员工文件夹里的既有总结文件

## 验收标准

- 你给出明确结论：`通过 / 有问题需返工`
- 若不通过，问题必须可复现、可回交
- 若通过，说明完整版本已进入可阶段验收状态
- 你在自己的文件夹下提交 [Phase13完整版本功能复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase13完整版本功能复验完成总结.md)

## 完成后必须提交

请在你的文件夹下新增：

- `Phase13完整版本功能复验完成总结.md`

总结里至少写清楚：

- 你复核了哪些能力
- 你执行了哪些命令
- 你的结论是通过还是不通过
- 如有缺陷，缺陷点是什么
