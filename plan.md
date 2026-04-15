# Implementation Plan: Phase 7 最终验收与后续排期

## Objective
在 Phase 6 收口已经完成的前提下，由项目经理输出最终验收口径、演示安排和后续排期建议，明确当前版本是否可以按阶段性交付通过验收。

## Context
- Triggered by: [员工/06_部署与文档工程师/Phase6部署与展示收口完成总结.md](/E:/sql-generator/员工/06_部署与文档工程师/Phase6部署与展示收口完成总结.md)
- Related work: [员工/05_测试工程师_QA/Phase5快速复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase5快速复验完成总结.md)、[docs/DEPLOYMENT.md](/E:/sql-generator/docs/DEPLOYMENT.md)、[docs/DEMO.md](/E:/sql-generator/docs/DEMO.md)、[docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
- Current verification:
  - `python -c "import app; print('app import ok')"` -> passed
  - `python -m pytest` -> `36 passed`
  - `python -m pytest tests/test_app_ui_regression.py -q` -> `7 passed`
  - `.streamlit/config.toml` -> added
  - `docs/DEPLOYMENT.md` / `docs/DEMO.md` / `LICENSE` -> added

## Open Questions
- 当前应按“阶段性交付”还是“完整长期愿景”做老板验收
- 漏斗分析、RFM 和真实部署结果应如何进入下一轮排期
- 最终演示时应如何避免老板误解未完成功能已交付

## Affected Modules

| Layer | Module | Change Type | Impact |
|-------|--------|-------------|--------|
| Docs | `plan.md` | Phase update | 当前执行依据 |
| Docs | `README.md` | Acceptance wording | 验收口径明确 |
| Docs | `docs/ROADMAP.md` | Phase update | 路线图推进 |
| Session | `SESSION.md` | Handoff update | 交接清晰 |
| PM | `员工/01_项目经理_产品负责人/项目完成总结.md` | Progress update | 项目总览同步 |
| PM | `员工/01_项目经理_产品负责人/Phase7最终验收与后续排期总结.md` | New file | 最终收口结论 |

## Verification
- 当前测试基线继续通过
- README、部署文档和演示文档口径一致
- 项目经理在个人文件夹下提交 [Phase7最终验收与后续排期总结.md](/E:/sql-generator/员工/01_项目经理_产品负责人/Phase7最终验收与后续排期总结.md)

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| 老板将“阶段性交付”误解为“完整长期愿景全部完成” | Medium | High | 明确区分两层验收口径 |
| 后续 backlog 未整理，导致项目虽然能验收但难以继续推进 | Medium | Medium | 输出下一轮优先级建议 |
| 演示时误碰未完成功能造成误判 | Medium | Medium | 演示严格按 `docs/DEMO.md` 进行 |

## Acceptance Criteria
- Phase 6 交付被项目经理确认通过
- 项目给出明确的最终验收口径
- 项目能明确区分“当前可验收范围”与“后续排期范围”
- 项目经理提交 `Phase7最终验收与后续排期总结.md`
- 共享进度文档与当前阶段保持一致

## Estimation Summary

| Metric | Value |
|--------|-------|
| Total backend modules affected | 0 |
| Total frontend modules affected | 0 |
| Migration required | No |
| API changes | No |
| Overall complexity | small |
