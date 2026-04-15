# SQL 分析模板生成器

`SQL 分析模板生成器` 是一个面向数据分析场景的轻量 Web 工具。用户输入表名、字段名和分析参数后，系统会生成可直接复用的分析 SQL，当前已完成趋势、同比 / 环比、留存三类核心分析的真实模板闭环，并提供 Streamlit 演示入口、历史记录、复制下载和最小自动化测试门禁。

## 当前状态

当前仓库已经完成：

- Day 1：项目骨架、统一入口、基础文档
- Day 2：趋势、同比 / 环比、留存分析 SQL 能力
- Day 5：Streamlit 交互闭环
- Day 7：QA 首轮回归与缺陷识别
- P1 修复：历史记录即时显示、失败后清理旧成功结果
- 最小 CI：GitHub Actions `pytest` 工作流
- Phase 5：QA 快速复验通过
- Phase 6：最小部署入口、部署说明、演示说明与 README 收口完成
- Phase 7：阶段验收口径与后续排期已整理完成
- Phase 8：mock data 数据包、参考 SQL 与外部平台验证说明已交付
- Phase 9：mock data 数据包快速复验通过
- 当前新增阶段已进入：`Phase 10 / 最终演示与老板验收`

当前验证基线：

- `python -c "import app; print('app import ok')"` -> passed
- `python -m pytest` -> `39 passed`

当前正在推进的下一步：

- 由项目经理基于现有材料完成最终演示安排和老板验收收口

## 已实现能力

- 趋势分析真实 SQL 生成
- 同比 / 环比真实 SQL 生成
- 留存宽表与留存曲线 SQL 生成
- `mysql` / `postgresql` 方言切换
- Streamlit 动态表单
- 结果展示、复制与下载
- 示例加载与历史记录回看
- GitHub Actions 最小 `pytest` CI 门禁
- Streamlit Community Cloud 最小部署入口
- mock data 数据包与外部平台验证说明

## 当前未实现能力

- 漏斗分析真实模板
- RFM 真实模板
- 真实数据库连接
- 真实线上部署结果与线上 URL
- 浏览器级 E2E 与完整发布流水线
- 平台内直接执行 SQL 与结果展示层

## 验收口径

- 如果按“当前演示版 / 阶段性交付”验收：`现在可以验收`
- 如果按“最初完整五类分析全部落地”验收：`尚未完全完成`

当前更准确的表述是：

- 趋势 / 对比 / 留存三类核心能力已经完成闭环
- 页面、测试、最小 CI、部署说明和演示材料已经齐备
- mock data 数据包已经补齐，并通过 QA 快速复验
- 漏斗分析与 RFM 已被明确留在后续排期，不应算作本轮已交付

## Tech Stack

- Python 3.11
- Streamlit
- Jinja2
- sqlparse
- PyYAML
- pytest
- GitHub Actions

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动应用

```bash
streamlit run app.py
```

### 3. 运行验证

```bash
python -c "import app; print('app import ok')"
python -m pytest
```

## 演示与部署入口

- 使用说明：[`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)
- 模拟数据验证：[`docs/MOCK_DATA_GUIDE.md`](docs/MOCK_DATA_GUIDE.md)
- 3 分钟上手：[`docs/QUICKSTART_3MIN.md`](docs/QUICKSTART_3MIN.md)
- 项目价值说明：[`docs/PRODUCT_VALUE.md`](docs/PRODUCT_VALUE.md)
- 部署说明：[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md)
- 演示说明：[`docs/DEMO.md`](docs/DEMO.md)
- 阶段路线图：[`docs/ROADMAP.md`](docs/ROADMAP.md)
- 架构说明：[`architecture.md`](architecture.md)

## 最小 CI 状态

仓库当前已接入最小 GitHub Actions `pytest` 工作流：

- 工作流文件：`.github/workflows/pytest.yml`
- 触发条件：`push`、`pull_request`
- 执行内容：
  - 安装 `requirements.txt`
  - 执行 `python -c "import app; print('app import ok')"` 冒烟检查
  - 执行 `python -m pytest`

当前 CI 的定位是“最小门禁”，不代表已覆盖 lint、部署、浏览器级 E2E 或 release。

## 项目结构

```text
sql-generator/
├── .github/
├── .streamlit/
├── app.py
├── architecture.md
├── plan.md
├── README.md
├── requirements.txt
├── SESSION.md
├── config/
├── core/
├── docs/
├── mock_data/
├── templates/
├── tests/
└── utils/
```

## 核心模块

### `app.py`

Streamlit 统一入口，负责表单输入、结果渲染、历史记录、错误提示、复制与下载交互。

### `core/generator.py`

统一 SQL 生成入口，负责模板映射、上下文构建、校验调用与格式化输出。

### `core/validator.py`

负责分析类型、方言、字段、聚合方式、日期范围、比较类型、留存参数等输入校验。

### `templates/`

存放各分析类型的 Jinja2 模板。当前 `trend.sql.j2`、`compare.sql.j2`、`retention.sql.j2` 已接入真实逻辑；`funnel.sql.j2` 与 `rfm.sql.j2` 仍保留为后续扩展。

### `mock_data/`

提供两张示例表、导入脚本、参考 SQL 和外部平台验证说明，用于验证页面当前三组示例 SQL。

## 本地演示建议

推荐在演示时按以下顺序操作：

1. 先展示趋势分析生成结果
2. 再展示同比 / 环比分析与方言切换
3. 再展示留存分析
4. 最后展示 mock data 验证包与外部平台验证说明

更完整的演示话术与顺序见 [`docs/DEMO.md`](docs/DEMO.md)。

## 当前建议

- 老板现在可以按“演示版 / 阶段性交付”做验收
- 如需进一步证明 SQL 可执行，优先使用 `docs/MOCK_DATA_GUIDE.md` 与 `mock_data/` 做外部平台验证
