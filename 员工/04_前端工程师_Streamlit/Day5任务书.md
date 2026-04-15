# Day 5 任务书：前端工程师（Streamlit）

## 你的角色
你是本项目当前阶段的关键执行人，负责把现有的 SQL 生成能力包装成一个可交互、可演示、可上手的 Streamlit 页面。

你这次工作的核心不是再写 SQL，而是让用户真正完成“输入参数 -> 生成 SQL -> 查看结果 -> 复制或下载”的闭环。

## 先看哪些文件
开始前请按顺序阅读以下文件：

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [architecture.md](/E:/sql-generator/architecture.md)
5. [app.py](/E:/sql-generator/app.py)
6. [core/generator.py](/E:/sql-generator/core/generator.py)
7. [core/validator.py](/E:/sql-generator/core/validator.py)
8. [员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md)
9. [员工/04_前端工程师_Streamlit/岗位职责说明.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/岗位职责说明.md)
10. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)

## 你要优先使用的 skills
- `developing-with-streamlit`
  用途：完成 `app.py` 的页面结构、交互布局、表单组织和结果区设计。
- `debugging-streamlit`
  用途：在页面联调时验证交互行为、排查 session_state 和控件问题。

## 你的 Day 5 具体任务

### 任务 1：改造主界面
请把当前 Day 1 占位页升级为可交互页面，至少包含：
- 分析类型选择
- SQL 方言选择
- 页面顶部使用说明
- 主区域动态表单
- 结果展示区域

当前优先接入的分析类型：
- 趋势分析
- 对比分析（同比 / 环比）
- 留存分析

### 任务 2：接入动态参数表单
请根据当前 `core/generator.py` 和 `core/validator.py` 已支持的参数，为 3 类分析提供输入组件：

趋势分析：
- `table_name`
- `date_field`
- `metric_field`
- `aggregation`
- `granularity`
- `date_range`
- `filter_conditions`

对比分析：
- 继承趋势分析主要参数
- 增加 `comparison_type`

留存分析：
- `table_name`
- `user_id_field`
- `date_field`
- `retention_days`
- `retention_mode`
- `start_date`
- `end_date`
- `filter_conditions`

### 任务 3：接入生成结果展示
请实现：
- 点击生成后调用统一入口 `SQLGenerator`
- 用 `st.code` 展示 SQL
- 多 SQL 结果使用 Tab 或其他清晰方式切换
- 支持复制到剪贴板
- 支持下载 `.sql` 文件

### 任务 4：实现交互增强
请补齐以下体验能力：
- 用 `st.session_state` 保存历史记录
- 支持历史回看
- 支持清空历史
- 首次进入显示欢迎说明
- 提供示例加载按钮
- 结果下方展示参数摘要

### 任务 5：基础错误处理
请保证：
- 参数不合法时显示明确提示
- 非法状态下禁用或阻止生成
- 不绕过后端校验器
- 页面结构简洁、适合演示

### 任务 6：提交完成总结
任务完成后，你必须在自己的文件夹下生成：
- [员工/04_前端工程师_Streamlit/Day5完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/Day5完成总结.md)

完成总结至少要包含：
- 本次完成了哪些文件
- 页面新增了哪些能力
- 如何验证
- 当前未做内容
- 推荐下一个对接人是谁以及原因

## 你交付时必须满足的验收标准
- 页面可以切换分析类型
- 页面可以输入参数并调用 `SQLGenerator`
- 页面可以展示 SQL 结果
- 至少支持复制和下载其中一种结果导出方式，目标是两种都支持
- 历史记录、示例加载、参数摘要具备基本可用性
- 已在个人文件夹生成 `Day5完成总结.md`

## 你现在不要做的事
- 不要绕过 `SQLGenerator` 自己拼 SQL
- 不要把 SQL 业务逻辑重新写进前端
- 不要提前接入漏斗和 RFM 的完整复杂表单
- 不要为了美化而牺牲清晰度和可维护性

## 项目经理对你的交接说明
SQL 工程师已经把趋势、同比环比、留存这三类分析能力接好了，你现在最重要的就是把这些能力变成用户真的能操作的界面。只要这一轮完成，我们就会得到第一版可以现场演示的闭环产品，这对后续 QA、文档和上线都会非常关键。

## 老板可以直接这样对你说
请你接手前端首轮闭环任务。先阅读 `SESSION.md`、`docs/ROADMAP.md`、`architecture.md`、`app.py` 以及 SQL 工程师的完成总结，再优先使用 `developing-with-streamlit` 和 `debugging-streamlit` 两个 skill。你的目标是把当前占位页面升级成可输入、可生成、可展示、可复制下载的交互页面，并在完成后在你的文件夹下提交 `Day5完成总结.md`。
