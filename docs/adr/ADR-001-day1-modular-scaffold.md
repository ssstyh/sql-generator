# ADR-001: Day 1 Modular Scaffold

## Status

Accepted

## Context

项目当前仍处于文档阶段，但 Day 2 起会有 SQL 工程师、前端工程师和 QA 并行接入。如果 Day 1 不先确定入口、模块边界和模板装载方式，后续很容易出现：

- UI 直接耦合模板文件
- 校验逻辑散落在多个模块
- 方言扩展位置不统一
- 新分析类型接入时需要重构目录

## Decision

采用模块化单体结构，固定以下边界：

- `app.py` 只做 Streamlit 入口和页面编排
- `core/generator.py` 作为唯一生成入口
- `core/validator.py` 负责基础校验
- `utils/formatter.py` 负责 SQL 格式化
- `templates/` 只存放 Jinja2 SQL 模板
- `core/db_connector.py` 仅负责 Day 1 的配置读取占位

## Consequences

正向影响：

- 后续员工可以直接在稳定目录中接力开发
- 模板、校验、格式化职责分离，便于测试
- MySQL / PostgreSQL 方言兼容有明确落点

负向影响：

- Day 1 生成结果仍以占位模板为主，业务价值有限
- 如果未来需求大幅膨胀，仍可能需要进一步拆分方言或服务层

## Alternatives Considered

### 方案一：先只写最小 `app.py`

- 优点：交付快
- 缺点：Day 2 需要重新设计结构，无法支撑多人协作

### 方案二：一开始就做复杂分层和方言抽象

- 优点：看起来更“完整”
- 缺点：超出 Day 1 范围，容易过度设计

## Follow-Up

- Day 2 起新增分析类型时，继续沿用本 ADR 的入口和目录约束
- 若方言差异显著增大，再追加新的 ADR 说明拆分策略
