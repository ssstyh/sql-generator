# Architecture: SQL 分析模板生成器

## Overview

项目当前已经完成完整版本的核心交付闭环：

- Day 1：搭建 Streamlit 入口、生成器、校验器、格式化器和模板目录骨架
- Day 2：落地趋势分析、同比环比、留存分析的真实 SQL 生成能力
- Day 5：接入动态表单、结果展示、历史记录、复制下载，形成第一版交互闭环
- Phase 4A：修复 QA 提出的两个页面层 P1 缺陷，恢复历史即时显示和失败后结果区清理
- Phase 4B：接入最小 GitHub Actions `pytest` CI，建立基础自动化门禁
- Phase 5：QA 快速复验通过，确认当前主流程与已修复 P1 场景无回退
- Phase 6：完成最小部署入口、部署说明、演示材料与仓库包装
- Phase 7：完成阶段验收口径统一与后续排期判断
- Phase 8：补齐 mock data 数据包、参考 SQL 与外部平台验证说明
- Phase 9：QA 已确认 mock data 数据包与当前示例参数一致，并通过快速复验
- Phase 11：SQL 工程师已补齐漏斗与 RFM 的核心 SQL 模板、校验与测试
- Phase 12：前端已把漏斗与 RFM 接到页面主链路
- Phase 13：QA 已确认完整版本五类分析主链路通过，完整版本具备阶段验收条件

当前架构已经进入最终收口阶段。也就是说，五类分析在代码和页面层都已经具备真实生成链路，当前剩余工作主要是统一最终验收口径与整理后续增强待办。

## Layer Structure

```text
Streamlit UI (app.py)
    -> Generator Facade (core/generator.py)
        -> Validator (core/validator.py)
        -> Template Loader (templates/*.sql.j2)
        -> Formatter (utils/formatter.py)
    -> Config Access (core/db_connector.py, config/db_config.yaml)
CI Gate (.github/workflows/pytest.yml)
    -> app import smoke test
    -> python -m pytest
Mock Validation Assets
    -> mock_data/*.csv
    -> mock_data/mysql/init.sql
    -> mock_data/postgresql/init.sql
    -> mock_data/reference_sql/*
    -> docs/MOCK_DATA_GUIDE.md
Full-Version Analysis Layer
    -> templates/funnel.sql.j2
    -> templates/rfm.sql.j2
    -> app.py funnel/rfm form + result rendering
```

## Module Responsibilities

### `app.py`

- 统一承接页面表单、按钮交互、结果渲染、历史记录和错误提示
- 当前已开放：趋势 / 对比 / 留存 / 漏斗 / RFM
- 仍有 1 个非阻塞 P2 文案口径待后续顺手修正，不影响当前功能验收

### `core/generator.py`

- 已统一支持五类分析的生成入口
- 页面层不应复制核心 SQL 逻辑，只负责正确传参与渲染结果

### `core/validator.py`

- 已覆盖五类分析所需关键校验
- funnel / rfm 的输入模型已固定为当前最小可用版本

### `templates/`

- `trend.sql.j2`
- `compare.sql.j2`
- `retention.sql.j2`
- `funnel.sql.j2`
- `rfm.sql.j2`

### `mock_data/`

- 当前主要服务趋势 / 对比 / 留存的外部平台验证
- 尚未扩展到漏斗 / RFM

## Key Decisions

- 演示版能力维持可验收状态
- 完整版本现在也已达到阶段验收条件
- 非阻塞 P2 文案问题不作为当前版本阻塞项
- 真实数据库连接与平台内执行层继续留在后续增强阶段，不并入本轮验收

## Request Flow

1. `app.py` 收集用户输入
2. UI 将分析类型、方言和参数提交给 `SQLGenerator`
3. `SQLGenerator` 调用 `InputValidator`
4. 校验通过后加载对应模板
5. 渲染结果交给 `SQLFormatter`
6. UI 负责展示、复制、下载和历史记录
7. `.github/workflows/pytest.yml` 对关键回归链路做持续门禁
8. mock data 资产支撑部分示例 SQL 的外部平台验证

## Current Scope Boundary

当前已完成：

- 五类分析的后端核心 SQL 能力
- 五类分析的页面入口与生成链路
- 历史记录、结果展示、最小 CI 门禁
- mock data 数据包与外部平台验证说明
- 自动化测试已达到 `46 passed`
- 演示版与完整版本都具备阶段性验收条件

当前仍未完成：

- 漏斗 / RFM 的 mock data 验证包
- 真实数据库连接
- 真实线上部署结果与线上 URL
- 浏览器级 E2E 与完整发布流水线
- 平台内直接执行 SQL 与结果展示层

## Next Steps

- 由项目经理统一完整版本最终验收口径与老板演示顺序
- 将 `app.py` 侧边栏旧文案 P2 记入验收后优化待办
- 如继续推进长期完整版，优先补漏斗 / RFM mock data、真实数据库连接与平台内执行能力
