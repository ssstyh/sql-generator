# Phase 11 漏斗与 RFM 核心能力任务书

## 你的身份

你是 `03_SQL模板与分析逻辑工程师`，本轮负责把完整版本里最关键的两项能力补齐：`漏斗分析` 和 `RFM 分析` 的真实 SQL 生成能力。

## 开始前先阅读

1. [plan.md](/E:/sql-generator/plan.md)
2. [docs/ROADMAP.md](/E:/sql-generator/docs/ROADMAP.md)
3. [SESSION.md](/E:/sql-generator/SESSION.md)
4. [README.md](/E:/sql-generator/README.md)
5. [architecture.md](/E:/sql-generator/architecture.md)
6. [app.py](/E:/sql-generator/app.py)
7. [core/generator.py](/E:/sql-generator/core/generator.py)
8. [core/validator.py](/E:/sql-generator/core/validator.py)
9. [templates/funnel.sql.j2](/E:/sql-generator/templates/funnel.sql.j2)
10. [templates/rfm.sql.j2](/E:/sql-generator/templates/rfm.sql.j2)
11. [员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Day2完成总结.md)

## 本轮必须优先使用的 skills

- `discover-database`
- `query-builder`

## 本轮任务目标

把当前仍处于“下一轮接入”状态的 `漏斗分析` 和 `RFM 分析`，补齐为真实可生成的 SQL 能力，并配套落下校验与测试。

## 你这轮要完成什么

### 1. 实现漏斗分析真实模板

至少完成：

- `templates/funnel.sql.j2` 的真实逻辑
- 与之匹配的参数校验
- 生成结果具有明确业务含义的输出字段

### 2. 实现 RFM 分析真实模板

至少完成：

- `templates/rfm.sql.j2` 的真实逻辑
- 与之匹配的参数校验
- 输出 recency / frequency / monetary 及可解释结果结构

### 3. 接好生成链路

确保这两类分析不再只是模板文件存在，而是真正能通过当前生成器链路走通：

- `core/generator.py`
- `core/validator.py`
- 如有必要的上下文构建逻辑

### 4. 补齐测试

至少补齐：

- 漏斗分析成功用例
- RFM 分析成功用例
- 关键参数校验失败用例

## 明确不要做什么

- 不要扩成真实数据库接入
- 不要这轮顺手做前端大改版
- 不要修改其他员工文件夹里的既有总结文件
- 不要回退当前 `39 passed` 的测试基线

## 验收标准

- 漏斗分析与 RFM 分析都能生成真实 SQL
- 校验器能正确拦截关键非法输入
- 测试基线继续通过，并新增这两类分析的测试覆盖
- 你在自己的文件夹下提交 [Phase11漏斗与RFM核心能力完成总结.md](/E:/sql-generator/员工/03_SQL模板与分析逻辑工程师/Phase11漏斗与RFM核心能力完成总结.md)

## 完成后必须提交

请在你的文件夹下新增：

- `Phase11漏斗与RFM核心能力完成总结.md`

总结里至少写清楚：

- 你修改了哪些模板 / 生成器 / 校验器 / 测试
- 漏斗与 RFM 各自的输入假设是什么
- 你本地怎么验证的
- 当前还剩哪些前端或 QA 后续工作
