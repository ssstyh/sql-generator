# Phase 6 部署与展示收口任务书

## 你的角色

你本轮以 `06_部署与文档工程师` 身份接手项目收尾阶段任务。目标不是新增业务功能，而是把当前已通过 QA 复验的版本整理成可部署、可展示、可交付说明的状态。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [.github/workflows/pytest.yml](/E:/sql-generator/.github/workflows/pytest.yml)
7. [员工/05_测试工程师_QA/Phase5快速复验完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Phase5快速复验完成总结.md)
8. [员工/02_技术负责人_后端架构师/最小CI接入完成总结.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/最小CI接入完成总结.md)
9. [员工/06_部署与文档工程师/岗位职责说明.md](/E:/sql-generator/员工/06_部署与文档工程师/岗位职责说明.md)
10. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)

## 本轮必须优先使用的 Skills

- `deployment-pipeline`
- `readme`

## 本轮任务目标

围绕当前已通过 QA 快速复验的版本，完成最小部署入口、README 收口、部署说明、演示材料与仓库包装。

## 具体要完成什么

### 1. 补最小部署入口

- 视当前仓库状态补齐 `.streamlit/config.toml`
- 保持配置最小、稳定，不要引入与当前功能无关的复杂选项

### 2. 收口 README

- 把 `README.md` 调整为更适合展示与交付的版本
- 明确写清：
  - 当前已实现能力
  - 当前未实现能力
  - 如何本地启动
  - 如何运行测试
  - 最小 CI 现状

### 3. 输出部署说明

- 在 `docs/` 下新增部署说明文件，建议命名为 `DEPLOYMENT.md`
- 至少写清：
  - 本地准备
  - Streamlit 部署入口
  - 依赖安装
  - 最小验证步骤

### 4. 输出演示材料说明

- 在 `docs/` 下新增演示说明文件，建议命名为 `DEMO.md`
- 至少写清：
  - 演示顺序
  - 推荐展示场景
  - 当前可展示功能
  - 当前不要误演示的未完成能力

### 5. 视情况补仓库包装

- 如仓库当前仍缺 `LICENSE`，请补最小可用版本
- 如你认为 `.gitignore`、展示说明或目录口径需要最小调整，可一并收口

## 范围控制

这轮不要做以下事情：

- 不新增业务功能
- 不修改 SQL 模板逻辑
- 不重新设计页面交互
- 不把本轮扩展成完整生产发布体系

## 交付物

你本轮至少要交付：

- `.streamlit/config.toml`（如当前确实缺失）
- `docs/DEPLOYMENT.md`
- `docs/DEMO.md`
- 收口后的 `README.md`
- `LICENSE`（如当前确实缺失）
- 你个人文件夹下的 [Phase6部署与展示收口完成总结.md](/E:/sql-generator/员工/06_部署与文档工程师/Phase6部署与展示收口完成总结.md)

## 完成总结要求

和之前的工程师一样，你在完成后必须在自己的文件夹下生成：

- `Phase6部署与展示收口完成总结.md`

总结里至少要写清楚：

- 你改了哪些文件
- 你补了哪些部署或文档材料
- 当前项目适合如何演示
- 还有哪些内容属于后续扩展，不应在本轮对外承诺
- 你建议下一步交给谁以及为什么

## 验收标准

- 部署与展示收口材料齐全
- 文档口径与当前代码能力一致
- 不夸大未完成能力
- 当前测试基线没有退化
- 你提交了 `Phase6部署与展示收口完成总结.md`
