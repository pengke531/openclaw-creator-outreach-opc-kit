# OpenClaw Creator Outreach OPC Kit

给已经安装好 OpenClaw 的用户使用。

这不是重装 OpenClaw 的项目，而是定义一套 **1主3执行** 的 creator outreach 架构，供客户本地 Codex 或人工按仓库文件手动配置到现有 OpenClaw 中。

## 当前正式架构

- `main` = Manager，唯一主控
- `wangcai` = Discovery 与 Evidence 执行
- `laicai` = Outreach 执行
- `facai` = ROI 复盘执行

系统层不是 agent：

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`

## 这版为什么这样设计

客户文件里真正需要的是：

- 1 个主控
- 1 个发现与核验执行
- 1 个外联执行
- 1 个 ROI 复盘执行

这版架构参考了 gstack 的正确部分：

- 一个 orchestrator
- 分阶段 owner
- 每阶段必须有交付物
- 重能力交给专职执行层

而不是照搬 gstack 的软件开发角色。

## 当前主路径

优先阅读：

- `MANUAL_CONFIGURATION_SPEC.md`

这份文件现在是手动配置的总规范。

## 推荐交付方式

优先采用：

1. 客户本地拉取这个仓库
2. 在仓库目录打开 Codex
3. 让 Codex 读取 `MANUAL_CONFIGURATION_SPEC.md`
4. 让 Codex 按仓库文件手动整理客户本地配置

## 核心仓库文件

客户本地 Codex 至少应读取：

- `MANUAL_CONFIGURATION_SPEC.md`
- `openclaw.json`
- `workspace/AGENTS.md`
- `workspace/MEMORY.md`
- `workspace/knowledge/creator-memory-and-state-model.md`
- `agents/wangcai/*`
- `agents/laicai/*`
- `agents/facai/*`
- `workspace/schemas/*`

## 仓库地址

`https://github.com/pengke531/openclaw-creator-outreach-opc-kit`
