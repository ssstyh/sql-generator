# Day 1 任务书：技术负责人 / 后端架构师

## 你的角色
你是本项目 Day 1 的主负责人，目标不是实现完整业务，而是把项目从“只有说明文档”推进到“具备可运行骨架和清晰架构边界”的状态。

## 先看哪些文件
开始前请按顺序阅读以下文件：

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [员工/02_技术负责人_后端架构师/岗位职责说明.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/岗位职责说明.md)
5. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)
6. [项目概述.md](/E:/sql-generator/项目概述.md)

## 你要优先使用的 skills
- `system-architecture`
  用途：先定义模块边界、核心调用关系、方言兼容思路和生成器职责划分。
- `python-project-structure`
  用途：把目录结构、包初始化、文件边界和测试放置方式搭好。

可选补充：
- `discover-database`
  只有在你需要提前统一 MySQL / PostgreSQL 方言差异和字段命名约束时再用。

## 你的 Day 1 具体任务

### 任务 1：输出基础架构说明
请先根据 `plan.md` 输出项目架构说明，至少明确：
- `app.py` 负责什么
- `core/generator.py` 负责什么
- `core/validator.py` 负责什么
- `utils/formatter.py` 负责什么
- `templates/` 中每类模板如何被统一调用
- 后续 SQL 工程师和前端工程师分别如何接入

建议产物：
- `architecture.md`

### 任务 2：完成项目骨架初始化
请创建以下结构并保证命名统一：

```text
sql-generator/
├── app.py
├── requirements.txt
├── README.md
├── config/
│   └── db_config.yaml
├── templates/
│   ├── retention.sql.j2
│   ├── funnel.sql.j2
│   ├── trend.sql.j2
│   ├── rfm.sql.j2
│   └── compare.sql.j2
├── core/
│   ├── __init__.py
│   ├── generator.py
│   ├── validator.py
│   └── db_connector.py
├── utils/
│   ├── __init__.py
│   └── formatter.py
└── tests/
    ├── test_generator.py
    └── test_validator.py
```

### 任务 3：完成最小可运行入口
`app.py` 先只做最小页面，要求：
- 使用 Streamlit
- 页面标题为“SQL 分析模板生成器”
- 可以被 `streamlit run app.py` 正常打开

### 任务 4：预留统一接口
请不要提前写复杂 SQL 逻辑，但必须把接口边界预留好：
- 生成器入口如何接收分析类型和参数
- 校验器如何做表名、字段名、聚合方式校验
- 格式化器如何统一处理 SQL 输出
- MySQL / PostgreSQL 方言差异准备放在哪一层

### 任务 5：补齐启动文档
请同步更新 `README.md`，至少包含：
- 项目简介
- 本地启动方式
- 当前目录结构说明
- Day 1 当前状态说明

## 你交付时必须满足的验收标准
- `streamlit run app.py` 可以打开页面
- `requirements.txt` 至少包含：`streamlit`、`jinja2`、`sqlparse`、`pyyaml`、`pyperclip`
- 项目目录结构与 `plan.md` 一致
- `architecture.md` 能帮助后续员工理解模块边界
- 后续 SQL 工程师拿到仓库后可以直接开始 Day 2 工作，而不需要重新整理项目结构

## 你现在不要做的事
- 不要提前实现趋势、留存、漏斗、RFM 的完整 SQL 逻辑
- 不要把 Day 5 的交互需求提前塞进 `app.py`
- 不要引入超出 MVP 范围的新框架
- 不要让目录结构为未来假想需求过度复杂化

## 项目经理对你的交接说明
这次我给你的目标很明确：先把地基搭好，不抢 Day 2 以后员工的工作。你现在最重要的成果不是“功能多”，而是“结构稳、边界清、后面的人能接得顺”。如果你完成后，SQL 工程师和前端工程师能直接接着干，那 Day 1 就算优秀完成。

## 老板可以直接这样对你说
请你接手 Day 1。先阅读 `plan.md`、`docs/ROADMAP.md`、`SESSION.md` 和你的岗位职责说明，再优先使用 `system-architecture` 与 `python-project-structure` 两个 skill，完成项目初始化、架构边界设计和最小可运行的 Streamlit 页面。今天的目标不是做完业务功能，而是把项目骨架、接口位置、依赖清单和 README 搭好，确保后面的 SQL 工程师能直接进入 Day 2 开发。
