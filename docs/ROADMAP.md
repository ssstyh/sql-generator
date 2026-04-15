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
| Phase 10 | 最终演示与老板验收 | 项目经理 | In Progress |

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
- [x] 扩展输入校验与测试
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
- [x] 技术负责人提交 `最小CI接入完成总结.md`

## Phase 5 - QA 快速复验与收口判断

Completed: 2026-04-15

- [x] QA 复核 `.github/workflows/pytest.yml` 口径
- [x] QA 重跑 `python -c "import app; print('app import ok')"`
- [x] QA 重跑 `python -m pytest`
- [x] QA 快速复验两个已修复的 P1 场景
- [x] QA 快速复验趋势 / 对比 / 留存主流程
- [x] QA 提交 `Phase5快速复验完成总结.md`

## Phase 6 - 部署、展示与剩余功能排期

Completed: 2026-04-15

- [x] 补齐 `.streamlit/config.toml`
- [x] 输出 `docs/DEPLOYMENT.md`
- [x] 输出 `docs/DEMO.md`
- [x] 收口 `README.md` 为展示版本
- [x] 补齐 `LICENSE`
- [x] 部署与文档工程师提交 `Phase6部署与展示收口完成总结.md`

## Phase 7 - 最终验收与后续排期

Completed: 2026-04-15

- [x] 项目经理确认当前项目的阶段性验收结论
- [x] 输出最终演示安排与老板验收口径
- [x] 明确“已完成范围”与“后续排期范围”
- [x] 整理漏斗分析、RFM 与真实部署的后续优先级
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
- [x] QA 提交 `Phase9模拟数据包快速复验完成总结.md`

## Phase 10 - 当前阶段：最终演示与老板验收

Goal: 由项目经理基于已通过的交付物和 QA 结论，完成老板演示安排、阶段验收结论和后续排期收口。

### Task Checklist

- [ ] 统一最终验收口径
- [ ] 明确老板演示顺序与展示重点
- [ ] 输出当前是否可验收的明确结论
- [ ] 明确后续排期边界
- [ ] 项目经理提交 `Phase10最终演示与老板验收完成总结.md`

### Definition of Done

- 老板可直接基于现有材料完成最终演示
- 项目经理给出明确验收结论
- 项目边界表达准确，不夸大未完成功能
