# SQL 分析模板生成器交付路线图

## Vision
这是一个面向数据分析场景的轻量 Web 工具。用户输入表名、字段名和分析参数后，系统自动生成可执行 SQL，用于趋势、同比环比、留存、漏斗和 RFM 五类常见分析。

## Who / Why
- 主要用户：数据分析师、数据运营、需要快速写分析 SQL 的个人开发者
- 核心价值：把重复性分析 SQL 的搭建时间从“半天重写”压缩到“几分钟生成”
- 约束条件：10 天 MVP、`Python + Streamlit + Jinja2`、可本地运行、可演示、可部署

## Scope
MVP 内建设：
- 趋势分析
- 同比环比分析
- 留存分析
- 漏斗分析
- RFM 分析
- Streamlit 交互界面
- 基础测试
- README 与部署材料

明确不在 v1 内建设：
- 用户登录和权限系统
- 真正的多用户协作
- 可视化图表编辑器
- 在线数据库写操作
- 复杂工作流编排

## Stack

| Layer | Choice | Why |
|-------|--------|-----|
| Frontend | Streamlit | 用最短路径做出可演示交互 |
| Backend | Python | 与模板生成、测试、格式化生态最匹配 |
| Template Engine | Jinja2 | 适合 SQL 模板复用和参数替换 |
| SQL Formatting | sqlparse | 输出结构统一，便于阅读和复制 |
| Config | YAML | 配置模板清晰易维护 |
| Testing | pytest | 易于参数化覆盖多种 SQL 场景 |
| Deployment | Streamlit Cloud | 适合 MVP 快速上线展示 |

## Build Order

| Phase | Goal | Owner | Sessions |
|-------|------|-------|----------|
| 1 | 完成项目骨架并能运行最小页面 | 技术负责人 | 1 |
| 2 | 落地趋势、同比环比、留存生成能力 | SQL 工程师 + 技术负责人 | 2 |
| 3 | 完成漏斗、RFM 与 Streamlit 主界面 | SQL 工程师 + 前端工程师 | 2 |
| 4 | 建立测试、文档、代码规范收口 | QA + 部署文档工程师 + 技术负责人 | 2 |
| 5 | 完成部署、Demo 模式与最终验收 | 部署文档工程师 + 项目经理 | 1-2 |

## Phase 1 - Day 1 项目初始化
Goal: 仓库从“说明文档”升级为“可运行项目骨架”。

### What's New
- Streamlit 主入口可启动
- 核心目录结构就位
- 依赖、模板、测试占位文件齐全
- README 具备快速启动说明

### Task Checklist
- [ ] 创建 `app.py`、`requirements.txt`、`config/`、`core/`、`templates/`、`utils/`、`tests/`
- [ ] 完成最小 Streamlit 标题页
- [ ] 建立生成器、校验器、格式化器占位接口
- [ ] 补齐 README 的项目简介与启动方式
- [ ] 验证本地可启动

### Definition of Done
- `streamlit run app.py` 能正常打开页面
- 仓库结构与项目概述保持一致
- Day 2 员工可以直接接手开发，不需要重新整理目录

## Phase 2 - Day 2 到 Day 4 核心分析能力
Goal: 产出第一批真正可用的 SQL 生成能力。

### What's New
- 趋势分析 SQL
- 同比与环比 SQL
- 留存分析 SQL

### Definition of Done
- 可生成 MySQL / PostgreSQL 两种方言 SQL
- 生成 SQL 带统一注释头
- 对关键输入项有校验
- 单元测试覆盖趋势与留存主路径

## Phase 3 - Day 4 到 Day 6 分析闭环与交互页
Goal: 让用户在页面内完成主要输入并看到生成结果。

### What's New
- 漏斗分析与 RFM 分析
- 动态表单和分析类型切换
- SQL 展示、复制、下载、历史记录

### Definition of Done
- 五类分析都能从 UI 触发
- 页面具备错误提示和示例加载
- 多 SQL 结果可以切换查看

## Phase 4 - Day 7 到 Day 8 测试与文档收口
Goal: 把项目从“能跑”推进到“可验证、可交接”。

### What's New
- pytest 测试套件
- README 完整版
- 代码注释、格式化、静态检查

### Definition of Done
- 关键分析场景有自动化测试
- README 可支持陌生人启动项目
- 代码规范达到可展示状态

## Phase 5 - Day 9 到 Day 10 部署与展示
Goal: 形成可演示、可上线、可用于面试展示的最终版本。

### What's New
- Streamlit Cloud 部署配置
- Demo 模式
- GitHub 包装与演示材料

### Definition of Done
- 项目具备可访问的演示入口
- README、截图、License、部署说明齐全
- 项目经理完成最终验收和演示脚本
