# Skills 分配清单

## 说明

本清单用于给 `SQL 分析模板生成器` 项目的 6 个员工分配可调用的 skills，方便每个岗位知道：

- 自己当前正式可用的是哪些 skills
- 在什么场景下应该优先调用哪一个 skill
- 哪些旧 skill 已被正式替代，不再作为主推荐

## 当前可用状态

### 已安装且正式推荐的 skills

- `project-planner`
- `discover-product`
- `roadmap`
- `system-architecture`
- `python-project-structure`
- `discover-database`
- `query-builder`
- `developing-with-streamlit`
- `debugging-streamlit`
- `pytest-patterns`
- `github-actions`
- `deployment-pipeline`
- `readme`

### 已保留但不再主推荐的旧 skills

- `project-manager`
- `product-manager`
- `project-session-management`

## 项目经理岗位替代关系

| 原 skill | 当前正式替代 skill | 说明 |
| --- | --- | --- |
| `project-manager` | `project-planner` | 用于项目拆解、阶段规划、里程碑和交付标准定义。 |
| `product-manager` | `discover-product` | 用于整理需求范围、功能优先级、用户价值和验收口径。 |
| `project-session-management` | `roadmap` | 用于跨阶段推进、跟踪当前进度、安排下一阶段动作。 |

## 员工与 Skills 对应表

| 员工 | Skill | 用途 |
| --- | --- | --- |
| 项目经理 / 产品负责人 | `project-planner` | 用于拆解 10 天排期、制定里程碑、安排负责人、明确阶段交付物。适合项目启动、阶段复盘和老板审查前调用。 |
| 项目经理 / 产品负责人 | `discover-product` | 用于明确 MVP、梳理功能优先级、定义用户价值和验收标准。适合做需求取舍和确认“先做什么”时调用。 |
| 项目经理 / 产品负责人 | `roadmap` | 用于按阶段推进项目、记录当前进展、整理阻塞和安排下一步。适合 Day 1 到 Day 10 的每日推进与收尾。 |
| 技术负责人 / 后端架构师 | `system-architecture` | 用于设计整体架构、模块边界、接口关系和关键技术取舍。适合 Day 1 架构设计和后续评审时调用。 |
| 技术负责人 / 后端架构师 | `python-project-structure` | 用于搭建 Python 项目目录、规划 `core`、`utils`、`templates`、`tests` 等结构。适合项目初始化和结构调整时调用。 |
| 技术负责人 / 后端架构师 | `discover-database` | 用于梳理字段语义、分析口径和 MySQL / PostgreSQL 差异，帮助统一参数和方言支持。 |
| SQL 模板与分析逻辑工程师 | `discover-database` | 用于理解表结构、字段语义、统计口径和业务指标定义，避免 SQL 逻辑建立在错误假设上。 |
| SQL 模板与分析逻辑工程师 | `query-builder` | 用于把趋势、同比、环比、留存、漏斗、RFM 等分析需求转成可执行 SQL 或 Jinja2 模板逻辑。 |
| 前端工程师（Streamlit） | `developing-with-streamlit` | 用于构建 Streamlit 主界面、动态表单、结果区、历史记录和下载交互，是前端开发的主 skill。 |
| 前端工程师（Streamlit） | `debugging-streamlit` | 用于排查 `session_state`、页面重复刷新、按钮失效、Tab 异常和联调问题。 |
| 测试工程师（QA） | `pytest-patterns` | 用于设计 pytest 测试结构、fixture、参数化测试、边界场景和回归测试。 |
| 测试工程师（QA） | `github-actions` | 用于把测试、校验和基础验收流程接入 GitHub 自动化，保证每次提交都能自动检查。 |
| 部署与文档工程师 | `deployment-pipeline` | 用于整理部署步骤、上线检查、发布门禁、验证流程和回滚方案。 |
| 部署与文档工程师 | `github-actions` | 用于编排持续集成、自动检查和部署相关工作流。 |
| 部署与文档工程师 | `readme` | 用于编写 README、快速开始、功能说明、部署说明、展示截图说明和仓库包装文案。 |

## 推荐调用顺序

### 项目启动阶段

1. 项目经理先调用 `project-planner`
2. 项目经理再调用 `discover-product`
3. 技术负责人调用 `system-architecture`
4. 技术负责人调用 `python-project-structure`

### 核心开发阶段

1. SQL 工程师先调用 `discover-database`
2. SQL 工程师再调用 `query-builder`
3. 前端工程师调用 `developing-with-streamlit`

### 联调与修复阶段

1. 前端工程师调用 `debugging-streamlit`
2. 测试工程师调用 `pytest-patterns`
3. 技术负责人和 QA 共同参考 `github-actions`

### 上线与展示阶段

1. 部署与文档工程师调用 `deployment-pipeline`
2. 部署与文档工程师调用 `readme`
3. 项目经理调用 `roadmap` 统筹最终收尾和审查节奏

## 使用建议

- 每个员工优先调用与自己岗位直接对应的主 skill
- 遇到跨岗位问题时，再补充调用相邻岗位的 skill
- 同一个问题优先调用 1 个主 skill，不够时再叠加第 2 个
- 后续如果继续扩展 skills，以这份清单为准，不再默认沿用旧的项目经理三件套
