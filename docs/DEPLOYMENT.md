# 部署说明

## 适用范围

本文档用于当前 `SQL 分析模板生成器` 的最小部署说明，目标是支撑演示级交付与 Streamlit Community Cloud 部署准备。

当前文档不代表：

- 已完成正式生产发布
- 已产出真实线上 URL
- 已验证数据库连接、浏览器级 E2E 或完整发布流水线

## 环境要求

- Python `3.11`
- 一个可访问的 GitHub 仓库
- 根目录 `requirements.txt`
- 根目录 `app.py`
- 已提交的 `.streamlit/config.toml`

## 本地准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 执行最小验证

```bash
python -c "import app; print('app import ok')"
python -m pytest
```

预期结果：

- `app import ok`
- `36 passed`

### 3. 本地启动应用

```bash
streamlit run app.py
```

启动后建议先验证以下页面能力：

- 趋势分析可生成 SQL
- 同比 / 环比可生成 SQL
- 留存分析可生成 SQL
- 复制与下载入口存在
- 侧边栏历史记录可回看
- 漏斗 / RFM 仍显示“真实模板仍在接入中”

## Streamlit Community Cloud 部署步骤

### 1. 准备仓库

确保以下文件已经推送到目标分支：

- `app.py`
- `requirements.txt`
- `.streamlit/config.toml`

### 2. 在 Streamlit Community Cloud 创建应用

在 Streamlit Community Cloud 中选择对应 GitHub 仓库后，按以下信息填写：

- Repository: 当前项目仓库
- Branch: 需要展示的目标分支
- Main file path: `app.py`

依赖安装会从根目录 `requirements.txt` 自动识别，应用运行时会读取 `.streamlit/config.toml` 中的最小服务端配置。

### 3. 首次启动后验证

部署页面可访问后，按以下顺序做最小验证：

1. 进入首页，确认页面可正常加载
2. 使用趋势分析示例生成 SQL
3. 切换到同比 / 环比分析并生成 SQL
4. 切换到留存分析并生成 SQL
5. 确认历史记录可回看
6. 确认漏斗 / RFM 仍为未开放状态，没有被误展示为已完成

## 回退说明

如果演示部署出现异常，不应在文档中写成“已上线成功”或“已完成正式发布”。本项目当前推荐的回退方式是：

1. 回退到最近一个本地已通过以下检查的提交
2. 重新部署该提交对应的仓库状态

建议回退前重新执行：

```bash
python -c "import app; print('app import ok')"
python -m pytest
```

## 当前不应承诺的事项

- 漏斗分析真实模板已完成
- RFM 真实模板已完成
- 已接入真实数据库
- GitHub Actions 已完成首次线上运行验证
- 已具备生产级监控、告警、灰度或自动回滚
