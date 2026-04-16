# SQL 分析模板生成器

`SQL 分析模板生成器` 是一个面向数据分析场景的轻量 Web 工具。用户输入表名、字段名和分析参数后，系统会生成可直接复用的分析 SQL。当前完整版本已经接通趋势、同比 / 环比、留存、漏斗和 RFM 五类分析，并完成页面交互、历史记录、复制下载、mock data 验证资产和最小自动化门禁。

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
- Phase 11：漏斗与 RFM 核心 SQL 能力已交付
- Phase 12：漏斗与 RFM 页面入口已开放
- Phase 13：完整版本功能复验通过
- 当前新增阶段已进入：`Phase 14 / 完整版本最终验收与收口`

当前验证基线：

- `python -c "import app; print('app import ok')"` -> `app import ok`
- `python -m pytest` -> `46 passed`

当前正在推进的下一步：

- 由项目经理统一完整版本最终验收口径、老板演示顺序与后续优化待办

## 已实现能力

- 趋势分析真实 SQL 生成
- 同比 / 环比真实 SQL 生成
- 留存宽表与留存曲线 SQL 生成
- 漏斗分析真实 SQL 生成
- RFM 分析真实 SQL 生成
- 五类分析统一页面入口与参数表单
- `mysql` / `postgresql` 方言切换
- Streamlit 动态表单
- 结果展示、复制与下载
- 示例加载与历史记录回看
- GitHub Actions 最小 `pytest` CI 门禁
- Streamlit Community Cloud 最小部署入口
- mock data 数据包与外部平台验证说明

## 当前未实现能力

- 漏斗 / RFM 的 mock data 验证包
- 真实数据库连接
- 真实线上部署结果与线上 URL
- 浏览器级 E2E 与完整发布流水线
- 平台内直接执行 SQL 与结果展示层

## 验收口径

- 如果按“当前演示版 / 阶段性交付”验收：`现在可以验收`
- 如果按“完整五类分析全部落地”验收：`现在也可以按阶段性交付口径验收`

当前更准确的表述是：

- 五类分析在代码和页面层都已接通
- QA 已确认完整版本主链路通过
- 当前版本已经具备“完整版本阶段验收”条件
- 但它仍不是“真实数据库直连、平台内执行 SQL、正式生产部署”的最终形态

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

## 当前建议

- 如果你要验收演示版：现在可以验收
- 如果你要验收完整版本：现在也可以按阶段性交付口径验收
- 如果你要继续做长期完整版：下一阶段应优先补漏斗 / RFM mock data、真实数据库连接与平台内执行能力
