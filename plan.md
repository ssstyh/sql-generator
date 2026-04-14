# Implementation Plan: Day 1 项目启动与骨架搭建

## Objective
在不扩大范围的前提下，先把 `SQL 分析模板生成器` 的 MVP 边界、Day 1 交付物和技术落地入口定义清楚，让团队能够从“项目说明”直接进入“可执行开发”。

## Context
- Triggered by: 仓库内现有的 [项目概述.md](/E:/sql-generator/项目概述.md)、[skills分配清单.md](/E:/sql-generator/skills分配清单.md)、[员工/人员配置总览.md](/E:/sql-generator/员工/人员配置总览.md)
- Related work: Day 1 的核心目标是完成项目初始化，形成一个可运行的 Streamlit 最小骨架，并为 Day 2 到 Day 10 保留稳定扩展路径

## Open Questions
- 漏斗分析是否只支持单表事件流，还是要在 MVP 内支持多表步骤输入
- `db_connector.py` 在 MVP 中是否只提供配置模板，还是要接入真实数据库探测
- SQL 标识符转义是否统一抽象成方言层能力，还是先在模板中局部处理
- Demo 模式的数据来源是静态示例参数，还是内置样例数据集

## Affected Modules

| Layer | Module | Change Type | Impact |
|-------|--------|-------------|--------|
| App | `app.py` | 新建 Streamlit 入口 | Day 1 可运行页面 |
| Config | `requirements.txt` | 新建依赖清单 | 本地启动与部署基础 |
| Config | `config/db_config.yaml` | 新建配置模板 | 数据源接入预留 |
| Backend | `core/__init__.py` | 新建包初始化 | 目录结构稳定 |
| Backend | `core/generator.py` | 新建生成器入口 | 后续 SQL 模板统一接入点 |
| Backend | `core/validator.py` | 新建校验入口 | 输入合法性控制 |
| Backend | `core/db_connector.py` | 新建数据库连接占位 | 后续扩展能力 |
| Utils | `utils/__init__.py` | 新建包初始化 | 工具层组织 |
| Utils | `utils/formatter.py` | 新建 SQL 格式化入口 | 输出一致性 |
| Templates | `templates/trend.sql.j2` | 新建模板占位 | 趋势分析扩展入口 |
| Templates | `templates/compare.sql.j2` | 新建模板占位 | 同比环比扩展入口 |
| Templates | `templates/retention.sql.j2` | 新建模板占位 | 留存分析扩展入口 |
| Templates | `templates/funnel.sql.j2` | 新建模板占位 | 漏斗分析扩展入口 |
| Templates | `templates/rfm.sql.j2` | 新建模板占位 | RFM 分析扩展入口 |
| Tests | `tests/test_generator.py` | 新建基础测试 | 生成器主流程回归 |
| Tests | `tests/test_validator.py` | 新建基础测试 | 校验逻辑回归 |
| Docs | `README.md` | 更新启动说明 | 对外理解与使用入口 |

## Verification
集成验证：
- 执行 `pip install -r requirements.txt`
- 执行 `streamlit run app.py`
- 浏览器中可打开页面并看到标题“SQL 分析模板生成器”

手工冒烟：
- 根目录结构与项目概述中的 Day 1 目标一致
- 依赖文件中至少包含 `streamlit`、`jinja2`、`sqlparse`、`pyyaml`、`pyperclip`
- 代码层已预留 `core/`、`templates/`、`utils/`、`tests/` 四类职责边界

回归要求：
- 新增文件命名清晰且可被后续员工直接复用
- 不引入与 Day 1 无关的业务复杂度

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Day 1 就把生成器细节做得过深，导致范围失控 | Medium | High | 严格限定为骨架、接口与占位，不提前展开 Day 2 以后逻辑 |
| 目录结构命名不统一，后续多人协作成本升高 | Medium | High | 由技术负责人统一模块职责与命名规范 |
| README 与实际结构不一致，后续交接混乱 | Medium | Medium | Day 1 同步更新 README，后续改动以 README 和路线图双向校验 |
| 漏斗、RFM、Demo 模式的边界未提前说明，后续返工 | Medium | Medium | 将其列为开放问题，由项目经理在 Day 2 前确认口径 |

## Acceptance Criteria
- 项目范围被明确锁定为 10 天 MVP，不额外扩展非核心功能
- Day 1 交付物、负责人、验收口径可直接执行
- 技术负责人拿到文档后可以不再反复追问目录、模块和接口边界
- 后续员工能够基于统一的骨架进入 SQL 模板开发、前端开发和测试工作

## Estimation Summary

| Metric | Value |
|--------|-------|
| Total backend modules affected | 6 |
| Total frontend modules affected | 1 |
| Migration required | No |
| API changes | No |
| Overall complexity | small |
