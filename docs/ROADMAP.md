# SQL 分析模板生成器交付路线图

## Vision

这是一个面向数据分析场景的轻量 Web 工具。用户输入表名、字段名和分析参数后，系统自动生成可执行 SQL，用于趋势、同比环比、留存、漏斗和 RFM 等常见分析。

## Build Order

| Phase | Goal | Owner | Status |
|-------|------|-------|--------|
| Phase 1 | 项目骨架与统一入口 | 技术负责人 | Completed |
| Phase 2 | 核心 SQL 能力接入 | SQL 工程师 | Completed |
| Phase 3 | Streamlit 交互闭环 | 前端工程师 | Completed |
| Phase 4A | QA 首轮回归与 P1 修复 | QA + 前端工程师 | Completed |
| Phase 4B | 最小 pytest CI 接入 | 技术负责人 | Completed |
| Phase 5 | QA 快速复验与收口判断 | QA + 项目经理 | Completed |
| Phase 6 | 部署、展示与剩余功能排期 | 部署文档工程师 + 项目经理 | Completed |
| Phase 7 | 最终验收与后续排期 | 项目经理 | Completed |
| Phase 8 | 模拟数据包交付与外部平台验证增强 | SQL 工程师 | Completed |
| Phase 9 | 模拟数据包快速复验 | QA | Completed |
| Phase 10 | 演示版最终验收准备 | 项目经理 | Ready |
| Phase 11 | 漏斗与 RFM 核心能力接入 | SQL 工程师 | Completed |
| Phase 12 | 前端开放漏斗与 RFM | 前端工程师 | Completed |
| Phase 13 | 完整版本功能复验 | QA | Completed |
| Phase 14 | 完整版本最终验收与收口 | 项目经理 | In Progress |

## Phase 1 - Day 1 项目初始化

Completed: 2026-04-14

- [x] 创建 `app.py`、`requirements.txt`、`config/`、`core/`、`templates/`、`utils/`、`tests/`
- [x] 建立最小 Streamlit 页面
- [x] 预留 `generator.py`、`validator.py`、`formatter.py`
- [x] 补齐基础 README 与架构说明

## Phase 2 - Day 2 到 Day 4 核心分析能力

Completed: 2026-04-14

- [x] 接入趋势分析 SQL
- [x] 接入同比 / 环比 SQL
- [x] 接入留存分析 SQL
- [x] 通过 `25 passed`

## Phase 3 - Day 5 到 Day 6 前端交互闭环

Completed: 2026-04-14

- [x] 动态表单
- [x] 结果展示
- [x] 复制与下载
- [x] 历史记录与示例加载
- [x] 通过 `29 passed`

## Phase 4A - Day 7 QA 与 P1 修复

Completed: 2026-04-14

- [x] QA 完成首轮系统化回归
- [x] 识别并记录 2 个页面层 P1 缺陷
- [x] 前端修复“历史记录不即时显示”
- [x] 前端修复“失败后残留旧成功结果”
- [x] 补充 UI 回归测试
- [x] 通过 `36 passed`

## Phase 4B - 最小 pytest CI 接入

Completed: 2026-04-14

- [x] 新增 `.github/workflows/pytest.yml`
- [x] 配置 `push` / `pull_request` 触发
- [x] 安装 `requirements.txt`
- [x] 执行 `python -m pytest`
- [x] 加入 `app import` 冒烟检查

## Phase 5 - QA 快速复验与收口判断

Completed: 2026-04-15

- [x] QA 复核 `.github/workflows/pytest.yml` 口径
- [x] QA 重跑 `python -c "import app; print('app import ok')"`
- [x] QA 重跑 `python -m pytest`
- [x] QA 快速复验两个已修复的 P1 场景
- [x] QA 快速复验趋势 / 对比 / 留存主流程

## Phase 6 - 部署、展示与剩余功能排期

Completed: 2026-04-15

- [x] 补齐 `.streamlit/config.toml`
- [x] 输出 `docs/DEPLOYMENT.md`
- [x] 输出 `docs/DEMO.md`
- [x] 收口 `README.md` 为展示版本
- [x] 补齐 `LICENSE`

## Phase 7 - 最终验收与后续排期

Completed: 2026-04-15

- [x] 项目经理确认当前项目的阶段性验收结论
- [x] 输出最终演示安排与老板验收口径
- [x] 明确“已完成范围”与“后续排期范围”
- [x] 响应新增需求，规划模拟数据增强阶段

## Phase 8 - 模拟数据包交付与外部平台验证增强

Completed: 2026-04-15

- [x] 交付 `mock_data/user_orders.csv` 与 `mock_data/user_events.csv`
- [x] 交付 MySQL / PostgreSQL `init.sql`
- [x] 交付 `mock_data/reference_sql/*`
- [x] 输出 `docs/MOCK_DATA_GUIDE.md`
- [x] 补充 `tests/test_mock_data_assets.py`
- [x] 测试基线提升到 `39 passed`

## Phase 9 - 模拟数据包快速复验

Completed: 2026-04-15

- [x] 复核 mock data 资产与说明文档
- [x] 复核当前三组示例参数与数据包一致性
- [x] 重跑 `python -m pytest`
- [x] 给出通过结论

## Phase 10 - 演示版最终验收准备

Ready: 2026-04-16

- 当前演示版已经具备老板验收条件
- 若老板按演示版 / 阶段性交付口径验收，可直接进入最终演示收口
- 当前该阶段被完整版本需求暂时后置，不代表演示版失效

## Phase 11 - 漏斗与 RFM 核心能力接入

Completed: 2026-04-16

- [x] 实现 `templates/funnel.sql.j2` 真实逻辑
- [x] 实现 `templates/rfm.sql.j2` 真实逻辑
- [x] 补齐 `core/generator.py` 与 `core/validator.py` 对应链路
- [x] 补齐漏斗 / RFM 测试
- [x] 测试基线提升到 `46 passed`

## Phase 12 - 前端开放漏斗与 RFM

Completed: 2026-04-16

- [x] 在 `app.py` 中开放 `funnel` 与 `rfm`
- [x] 补齐对应参数表单与结果展示
- [x] 保持历史记录、示例加载与生成链路可用
- [x] 补齐 UI 回归测试

## Phase 13 - 完整版本功能复验

Completed: 2026-04-16

- [x] 重跑完整测试基线
- [x] 复验 funnel / rfm 页面可生成链路
- [x] 检查历史记录、结果展示与旧功能是否回退
- [x] QA 给出“通过”结论
- [x] 记录 1 个非阻塞 P2 旧文案问题

## Phase 14 - 当前阶段：完整版本最终验收与收口

Goal: 由项目经理统一完整版本最终验收口径、老板演示顺序和后续增强待办，正式完成本轮项目收口。

### Task Checklist

- [ ] 给出完整版本是否可阶段验收的正式结论
- [ ] 统一 README / ROADMAP / SESSION / architecture / 项目完成总结口径
- [ ] 明确非阻塞 P2 为验收后优化待办
- [ ] 提交 `Phase14完整版本最终验收与收口完成总结.md`

### Definition of Done

- 完整版本被正式判定为可阶段验收
- 共享文档口径一致
- 后续增强项与非阻塞问题被清晰记录
