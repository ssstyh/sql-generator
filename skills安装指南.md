# Skills 安装指南

## 目的

本指南用于解决本机在安装 Codex skills 时常见的网络、代理、仓库路径和安装方式问题，帮助后续稳定、高效地安装 skills，避免重复踩坑。

## 当前环境结论

经过本次排查，当前机器的稳定安装前提如下：

- Clash Verge 实际可用的本地混合代理端口是 `7897`
- Windows 系统代理当前指向 `127.0.0.1:7897`
- `npm` 已切换到官方源：`https://registry.npmjs.org`
- PowerShell 登录时会自动修复错误代理 `127.0.0.1:9`

因此，后续建议优先在 `PowerShell` 中执行 skills 安装命令。

## 已确认的高频问题

### 1. 错误代理被注入到终端

此前最主要的问题是终端里出现了错误代理：

```text
HTTP_PROXY=http://127.0.0.1:9
HTTPS_PROXY=http://127.0.0.1:9
ALL_PROXY=http://127.0.0.1:9
```

这会导致：

- GitHub 仓库下载失败
- `npx` 和 `npm` 请求异常
- 安装脚本反复超时或误报

### 2. 仓库路径不一定在根目录

很多 skills 并不在仓库根目录，而是在类似下面的位置：

- `skills/<skill-name>/`
- `plugins/.../skills/<skill-name>/`
- `cli/skills/<skill-name>/`
- `._archive/.../<skill-name>/`

如果路径写错，即使仓库能访问，安装也会失败。

### 3. skills.sh 页面和 GitHub 仓库可能不完全一致

有些 skills 在技能导航页能看到，但原始仓库：

- 可能已删除
- 可能改名
- 可能仓库私有化
- 可能 skill 实际路径变更

所以安装前最好先确认 GitHub 仓库可访问且路径真实存在。

### 4. `npx skills add` 不一定是最快最稳的方法

在网络一般、代理复杂、仓库结构不统一时，`npx skills add` 容易：

- 触发交互问题
- 因 npm registry 或镜像源异常失败
- 因仓库结构复杂无法直接找到 skill

因此更推荐优先使用官方安装脚本，必要时直接手动稀疏拉取。

## 推荐安装顺序

后续安装 skills 时，建议按以下顺序执行。

### 第一步：确认 Clash Verge 正在运行

确认 Clash Verge 已打开，并且混合端口仍然是 `7897`。

如需检查，可看：

```text
C:\Users\31514\AppData\Roaming\io.github.clash-verge-rev.clash-verge-rev\config.yaml
```

重点看：

```yaml
mixed-port: 7897
```

### 第二步：在 PowerShell 中确认代理已正确生效

执行：

```powershell
Write-Output $env:HTTP_PROXY
Write-Output $env:HTTPS_PROXY
Write-Output $env:ALL_PROXY
```

期望结果：

```text
http://127.0.0.1:7897
```

如果不是，就手动补一次：

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
$env:ALL_PROXY='http://127.0.0.1:7897'
```

### 第三步：先确认仓库是否可访问

用 Git 先测，不要直接盲装：

```powershell
git ls-remote https://github.com/OWNER/REPO.git HEAD
```

如果返回 commit 哈希，说明仓库本身可访问。

### 第四步：确认 skill 的真实路径

不要默认 skill 在仓库根目录。

推荐方法：

```powershell
git clone --depth 1 --filter=blob:none --no-checkout https://github.com/OWNER/REPO.git $tmp
git -C $tmp ls-tree -r --name-only HEAD | Select-String 'SKILL.md|skill-name'
```

根据输出找到真实路径，例如：

- `skills/project-planner`
- `cli/skills/query-builder`
- `plugins/dev-tools/skills/roadmap`

### 第五步：优先使用官方安装脚本

官方脚本路径：

```text
C:\Users\31514\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py
```

推荐命令模板：

```powershell
$env:HTTP_PROXY='http://127.0.0.1:7897'
$env:HTTPS_PROXY='http://127.0.0.1:7897'
$env:ALL_PROXY='http://127.0.0.1:7897'

python C:\Users\31514\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo OWNER/REPO `
  --path ACTUAL/SKILL/PATH `
  --name SKILL_NAME `
  --method download
```

如果下载模式失败，再试：

```powershell
python C:\Users\31514\.codex\skills\.system\skill-installer\scripts\install-skill-from-github.py `
  --repo OWNER/REPO `
  --path ACTUAL/SKILL/PATH `
  --name SKILL_NAME `
  --method git
```

## 最稳的手动安装方法

如果官方安装脚本有问题，最稳的方法是手动稀疏拉取后复制。

### 适用场景

- 安装脚本报错但仓库能访问
- 仓库路径复杂
- 安装脚本临时目录冲突
- 只想安装某一个 skill，不想整仓下载

### 操作步骤

#### 1. 先备份已有同名 skill

```powershell
Rename-Item `
  -LiteralPath C:\Users\31514\.codex\skills\SKILL_NAME `
  -NewName ('SKILL_NAME.backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
```

#### 2. 稀疏拉取仓库

```powershell
$tmp = Join-Path $env:TEMP ('skill-sparse-' + [guid]::NewGuid().ToString())
git clone --depth 1 --filter=blob:none --sparse https://github.com/OWNER/REPO.git $tmp
git -C $tmp sparse-checkout set ACTUAL/SKILL/PATH
```

#### 3. 复制 skill 到本地目录

```powershell
Copy-Item `
  -LiteralPath (Join-Path $tmp 'ACTUAL\\SKILL\\PATH') `
  -Destination C:\Users\31514\.codex\skills\SKILL_NAME `
  -Recurse
```

#### 4. 检查是否安装成功

```powershell
Get-ChildItem C:\Users\31514\.codex\skills\SKILL_NAME
Get-Content C:\Users\31514\.codex\skills\SKILL_NAME\SKILL.md -TotalCount 20
```

## 失败时的排障顺序

以后如果安装失败，按下面顺序排查最快。

### A. 先看代理是否正确

```powershell
Write-Output $env:HTTP_PROXY
Write-Output $env:HTTPS_PROXY
Write-Output $env:ALL_PROXY
```

如果看到 `127.0.0.1:9`，说明代理又错了。

### B. 看 Clash 端口是否在监听

```powershell
netstat -ano | Select-String ':7897'
```

如果没监听，说明 Clash Verge 没正常工作。

### C. 看 GitHub 是否可达

```powershell
git ls-remote https://github.com/OWNER/REPO.git HEAD
```

### D. 看是不是路径写错

```powershell
git -C $tmp ls-tree -r --name-only HEAD | Select-String 'skill-name|SKILL.md'
```

### E. 看是不是安装器自身 bug

如果报临时目录冲突、下载模式异常、稀疏检出失败，可以直接改走“手动安装法”。

## 建议保留的习惯

- 安装前先确认仓库可访问
- 安装前先确认真实路径
- 安装前先备份旧 skill
- 优先用官方脚本
- 脚本失败就直接手动稀疏拉取
- 安装完统一重启 Codex

## 当前项目经理替代 Skills 建议

由于原先匹配的 3 个来源不可用或路径无法公开确认，当前建议改用以下公开可访问的替代 skills：

| 原目标 skill | 建议替代 skill | 用途 |
| --- | --- | --- |
| `project-manager` | `project-planner` | 用于排期、任务拆解、验收标准和复杂度判断 |
| `product-manager` | `discover-product` | 用于产品需求、优先级、PRD 和验收口径 |
| `project-session-management` | `roadmap` | 用于阶段推进、跨会话执行和持续交付路线图 |

## 安装完成后的最后一步

所有新安装或替换的 skills，只有在 `Codex 重启后` 才能稳定被新会话识别。

因此建议：

1. 先完成一轮安装
2. 再统一重启 Codex
3. 重启后再开始正式调用新 skills
