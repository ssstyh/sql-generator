# 最小 CI 接入任务书

## 你的角色

你本轮以 `02_技术负责人_后端架构师` 身份接手项目收口阶段任务。目标不是扩展业务功能，而是在当前功能基线已经稳定的情况下，为仓库补上最小 GitHub Actions `pytest` CI。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [员工/05_测试工程师_QA/Day7完成总结.md](/E:/sql-generator/员工/05_测试工程师_QA/Day7完成总结.md)
7. [员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md](/E:/sql-generator/员工/04_前端工程师_Streamlit/P1缺陷修复完成总结.md)
8. [员工/02_技术负责人_后端架构师/岗位职责说明.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/岗位职责说明.md)
9. [skills分配清单.md](/E:/sql-generator/skills分配清单.md)

## 本轮必须优先使用的 Skills

- `github-actions`
- `system-architecture`

## 本轮任务目标

为当前仓库新增最小 GitHub Actions 工作流，把现有 `pytest` 回归测试纳入自动化校验。

## 具体要完成什么

### 1. 新增最小工作流

- 在 `.github/workflows/` 下新增工作流文件
- 建议命名为 `pytest.yml`
- 触发条件至少包含：
  - `push`
  - `pull_request`

### 2. 工作流内容保持最小且稳定

- 配置 Python 运行环境
- 安装 `requirements.txt`
- 执行 `python -m pytest`
- 如你判断稳定且必要，可补一个 `python -c "import app; print('app import ok')"` 冒烟检查

### 3. 范围控制

这轮不要做以下事情：

- 不新增业务功能
- 不改分析模板范围
- 不重构 `app.py` 主逻辑
- 不顺手扩展部署、lint、release 流程

## 交付物

你本轮至少要交付：

- `.github/workflows/pytest.yml`
- 必要的最小文档同步
- 你个人文件夹下的 [最小CI接入完成总结.md](/E:/sql-generator/员工/02_技术负责人_后端架构师/最小CI接入完成总结.md)

## 完成总结要求

和前端工程师一样，你在完成后必须在自己的文件夹下生成：

- `最小CI接入完成总结.md`

总结里至少要写清楚：

- 你改了哪些文件
- 工作流触发条件是什么
- 工作流具体执行了哪些步骤
- 本地做了哪些验证
- 还剩哪些风险或后续建议

## 验收标准

- 仓库新增最小 GitHub Actions `pytest` 工作流
- 工作流职责单一，围绕测试校验
- 本地 `python -m pytest` 继续通过
- 本地 `python -c "import app; print('app import ok')"` 继续通过
- 你提交了 `最小CI接入完成总结.md`

## 你可以直接按这个口径执行

“本轮只做最小 CI 接入，不扩需求，不扩架构，不改功能边界。目标是把当前 36 项通过的测试纳入 GitHub Actions，形成项目收口前的自动化门禁。”
