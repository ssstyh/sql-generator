# Architecture: SQL 分析模板生成器

## Overview

项目当前已经完成九个关键阶段：

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

因此当前架构重点已经从“让 SQL 能生成并可验证”推进到“基于现有闭环完成最终演示与老板验收”。

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
```

## Module Responsibilities

### `app.py`

- 统一承接页面表单、按钮交互、结果渲染、历史记录和错误提示
- 所有 SQL 生成请求都通过 `SQLGenerator` 发起
- 当前三组 `EXAMPLES` 已作为 mock data 资产的唯一对齐基准

### `core/generator.py`

- 作为统一生成入口，负责：
  - 分析类型与模板文件映射
  - 调用 `InputValidator`
  - 加载 `templates/*.sql.j2`
  - 注入公共上下文
  - 调用 `SQLFormatter`

### `core/validator.py`

- 负责输入合法性校验
- 当前已覆盖趋势、对比、留存所需的关键参数约束
- 后续漏斗和 RFM 接入时，应继续在这里补充校验规则

### `utils/formatter.py`

- 负责 SQL 输出格式统一
- 避免模板层和 UI 层直接处理格式化细节

### `core/db_connector.py`

- 当前仍为配置读取占位模块
- 本阶段仍不接真实数据库连接，保持架构边界清晰

### `templates/`

- `trend.sql.j2`
- `compare.sql.j2`
- `retention.sql.j2`
- `funnel.sql.j2`：待后续实现
- `rfm.sql.j2`：待后续实现

### `.github/workflows/pytest.yml`

- 当前最小 CI 门禁文件
- 在 `push` / `pull_request` 下触发
- 负责安装依赖、做 `app import` 冒烟检查，并执行全量 `pytest`

### `mock_data/`

- 提供 `user_orders` 与 `user_events` 两张示例表数据
- 提供 MySQL / PostgreSQL 初始化脚本
- 提供参考 SQL 与外部平台验证说明
- 目标是让页面示例 SQL 可以被老板或新手直接拿到外部平台验证

## Key Decisions

- 保持单仓库、单入口的模块化单体结构
- 统一通过 `SQLGenerator.generate()` 提供生成能力
- 校验和格式化从模板层剥离
- 页面层只负责交互，不直接读模板，也不复制校验逻辑
- 最小 CI 先聚焦 `app import` 与 `pytest`
- mock data 资产优先服务“外部平台验证”，而不是直接做平台内执行层

## Request Flow

1. `app.py` 收集用户输入
2. UI 将分析类型、方言和参数提交给 `SQLGenerator`
3. `SQLGenerator` 调用 `InputValidator`
4. 校验通过后加载对应模板
5. 渲染结果交给 `SQLFormatter`
6. UI 负责展示、复制、下载和历史记录
7. `.github/workflows/pytest.yml` 对关键回归链路做持续门禁
8. `mock_data/*` 与 `docs/MOCK_DATA_GUIDE.md` 为示例 SQL 提供外部平台验证闭环
9. QA 已确认这套验证资产足以支撑老板演示与外部平台验证

## Current Scope Boundary

当前已完成：

- 项目结构稳定
- 趋势 / 对比 / 留存 SQL 可生成
- 页面可输入、可生成、可展示、可复制下载
- 两个 QA 识别的 P1 页面问题已修复
- 最小 GitHub Actions `pytest` CI 已接入
- 自动化测试已达到 `39 passed`
- mock data 数据包与外部平台验证说明已落地
- 当前演示版已具备阶段性验收条件

当前未完成：

- 漏斗分析与 RFM 真模板
- 真实数据库连接
- 真实线上部署结果与线上 URL
- 浏览器级 E2E 与完整发布流水线
- 平台内直接执行 SQL 与结果展示层

## Next Steps

- 由项目经理完成最终演示与老板验收收口
- 根据老板结论，决定是当前阶段验收通过，还是继续进入下一轮扩展排期
