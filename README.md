# OpenClaw Creator Outreach OPC Kit

给已经安装好 OpenClaw 的用户使用。

这不是重装 OpenClaw 的项目，而是把一套 Creator Outreach Agent 架构增量导入到现有 OpenClaw 中。

## 别人怎么用

前提：

- 对方已经装好 OpenClaw
- `openclaw` 命令可以正常使用

然后只做一件事：

### Windows

```powershell
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
powershell -ExecutionPolicy Bypass -File .\import.ps1
```

### macOS / Linux / WSL2

```bash
git clone https://github.com/pengke531/openclaw-creator-outreach-opc-kit
cd openclaw-creator-outreach-opc-kit
chmod +x ./import.sh
./import.sh
```

## 运行这一个命令后会发生什么

`import` 会自动完成：

- 预检
- 增量导入架构
- 合并 OpenClaw 配置
- 创建 Creator Outreach 域目录
- 注入 4 个 Agent
- 验证配置
- 如果 gateway 已在运行，自动做 smoke test

也就是说，对普通用户来说，默认只需要跑一次 `import`。

## 导入成功后会得到什么

会新增这 4 个 Agent：

- `creator_manager`
- `creator_scout`
- `creator_connector`
- `creator_analyst`

会新增这个目录：

```text
~/.openclaw/domains/creator-outreach-opc
```

## 如果导入时提示 gateway 没启动

那就再执行：

```bash
openclaw gateway
```

然后重新运行刚才那个 `import` 命令即可。

## 这套架构适合谁

适合已经有 OpenClaw、现在只想增量导入一套创作者商务投放架构的人。

## 仓库地址

仓库地址就是：

`https://github.com/pengke531/openclaw-creator-outreach-opc-kit`
