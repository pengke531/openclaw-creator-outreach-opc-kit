# OpenClaw Creator Outreach OPC Kit

给已经安装好 OpenClaw 的用户使用。

这不是重装 OpenClaw 的项目，而是定义一套 **旺财双层主控架构**，供客户本地 Codex 或人工按仓库文件手动配置到现有 OpenClaw 中。

## 架构概览

- `main` = 旺财，唯一主控
- `laicai` = 外联执行
- `facai` = ROI 复盘

系统层不是 agent：

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`

## 当前主路径

优先阅读：

- `MANUAL_CONFIGURATION_SPEC.md`

这份文件现在是手动配置的总规范。

## 推荐交付方式

优先采用：

- 客户本地打开 Codex
- Codex 进入这个仓库目录
- Codex 只依据仓库里的架构文件和配置文件手动整理客户本地配置

详细执行协议见：

- `CUSTOMER_LOCAL_IMPORT.md`

这条路径是当前仓库的主交付方式。`import.ps1` / `import.sh` 只保留为辅助入口，不再作为推荐交付依赖。

## 别人怎么用

前提：

- 对方已经装好 OpenClaw
- `openclaw` 命令可以正常使用

### 方式 A：客户本地 Codex 导入

1. 让客户先把仓库拉到本地
2. 在这个仓库目录打开 Codex
3. 让 Codex 按 `CUSTOMER_LOCAL_IMPORT.md` 的要求执行本地导入

建议直接把 `CUSTOMER_LOCAL_IMPORT.md` 里的整段执行要求发给客户本地 Codex。

### 方式 B：辅助脚本导入

#### Windows

```powershell
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
powershell -ExecutionPolicy Bypass -File .\import.ps1
```

#### macOS / Linux / WSL2

```bash
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
chmod +x ./import.sh
./import.sh
```

## 导入后会得到什么

`~/.openclaw/domains/creator-outreach-opc` 下会出现：

- `workspace`
- `agents/laicai`
- `agents/facai`

`~/.openclaw/openclaw.json` 里会存在：

- `main`
- `laicai`
- `facai`

说明：

- `main` 会被这套场景架构重定义为旺财主控
- `laicai` 和 `facai` 是旺财唯一允许调度的子 agent

## 如何判断导入成功

检查：

```text
C:\Users\你的用户名\.openclaw\domains\creator-outreach-opc
```

应该至少能看到：

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`
- `agents/laicai`
- `agents/facai`

## 如果 gateway 还在启动

出现 `GatewayRequestError: chat.history unavailable during gateway startup`
时，不要先判断导入失败。

先检查目录和 `openclaw.json` 是否已经落地；如果已落地，等 gateway 完全启动后再执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\verify-creator-outreach.ps1
```

## 仓库地址

`https://github.com/pengke531/openclaw-creator-outreach-opc-kit`
