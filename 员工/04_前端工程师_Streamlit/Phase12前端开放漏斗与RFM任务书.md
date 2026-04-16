# Phase 12 前端开放漏斗与 RFM 任务书

## 你的身份

你是 `04_前端工程师_Streamlit`，本轮负责把 SQL 工程师已经落地的 `漏斗分析` 与 `RFM 分析` 核心能力接到页面里，让这两类分析从“后端已支持”变成“页面可用”。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [app.py](/E:/sql-generator/app.py)
7. [core/generator.py](/E:/sql-generator/core/generator.py)
8. [core/validator.py](/E:/sql-generator/core/validator.py)
9. [员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力完成总结.md)

## 本轮必须优先使用的 skills

- `developing-with-streamlit`
- `debugging-streamlit`

## 本轮任务目标

把 `漏斗分析` 与 `RFM 分析` 从当前页面里的“下一轮接入”状态，升级为真正可输入、可生成、可展示、可纳入历史记录的前端能力。

## 你这轮要完成什么

### 1. 打开漏斗与 RFM 的前端入口

至少包括：

- 在 `app.py` 中开放 `funnel` 与 `rfm`
- 调整 `ANALYSES` / `UI_ANALYSES` 与相关提示文案
- 让这两类分析不再显示“接入中”提示

### 2. 补齐参数表单

至少完成：

- 漏斗分析所需参数输入
- RFM 分析所需参数输入
- 与 SQL 工程师本轮固定的输入模型保持一致

### 3. 接好结果展示链路

至少确认：

- 页面可成功触发 SQL 生成
- 结果区能展示漏斗 / RFM 的 SQL
- 参数摘要、历史记录、示例加载等链路不被破坏

### 4. 补齐前端回归测试

至少补：

- funnel 可生成的 UI 路径
- rfm 可生成的 UI 路径
- 如有必要，更新原先“接入中”断言相关测试

## 明确不要做什么

- 不要在这一轮推进真实数据库连接
- 不要顺手把 mock data 扩到漏斗 / RFM
- 不要修改其他员工文件夹里的既有总结文件
- 不要回退当前 `46 passed` 的测试基线

## 验收标准

- 页面中已开放漏斗分析与 RFM 分析
- 用户可在页面填写参数并生成 SQL
- 现有趋势 / 对比 / 留存链路不回退
- 测试基线继续通过，并补齐必要 UI 回归
- 你在自己的文件夹下提交 [Phase12前端开放漏斗与RFM完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/Phase12前端开放漏斗与RFM完成总结.md)

## 完成后必须提交

请在你的文件夹下新增：

- `Phase12前端开放漏斗与RFM完成总结.md`

总结里至少写清楚：

- 你修改了哪些页面逻辑与测试
- 漏斗 / RFM 的页面输入方式如何对应后端输入模型
- 你本地如何验证的
- 当前还剩哪些 QA 或数据资产后续工作
