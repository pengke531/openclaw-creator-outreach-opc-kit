# Customer Local Import Protocol

这个仓库现在作为 **唯一事实源**。

目标不是让客户双击脚本碰运气，而是：

- 客户本地打开 Codex
- Codex 只依据当前仓库文件
- 在客户本机把架构导入到当前用户的 OpenClaw
- 完成备份、合并、校验、验证

## 适用前提

- 客户机器已经安装并能运行 OpenClaw
- 仓库已经拉到客户本地
- 客户本地可以打开 Codex 并进入这个仓库目录

## 仓库中的权威文件

导入时只信这些文件：

- `openclaw.json`
- `workspace/AGENTS.md`
- `workspace/MEMORY.md`
- `agents/laicai/*`
- `agents/facai/*`
- `workspace/registry/*`
- `workspace/evidence/*`
- `workspace/inbox/*`
- `workspace/schemas/*`
- `workspace/templates/*`

## 本地导入目标

导入到：

```text
~/.openclaw/domains/creator-outreach-opc
```

并把以下 agent 合并进当前用户的 `~/.openclaw/openclaw.json`：

- `main`
- `laicai`
- `facai`

## 目标架构

- `main` = Manager，唯一主控
- `wangcai` = 侦察与证据执行
- `laicai` = 外联执行
- `facai` = ROI/复盘

系统层：

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`

## 客户本地给 Codex 的执行要求

在客户本地打开 Codex 后，直接让它执行下面这段要求：

```text
请基于当前仓库文件，把这套 creator-outreach 架构导入到当前用户的 OpenClaw 本地环境。

要求：
1. 不下载外部仓库，不依赖仓库外的技能目录，不假设本机已有额外 skills。
2. 先备份当前 ~/.openclaw/openclaw.json。
3. 将当前仓库中的架构文件导入到 ~/.openclaw/domains/creator-outreach-opc。
4. 将 openclaw.json 中定义的 main / wangcai / laicai / facai 合并进当前用户配置。
5. main 必须是唯一主控，允许调度 wangcai、laicai 和 facai。
6. registry / evidence / inbox 目录必须完整存在。
7. 导入后执行配置校验。
8. 输出最终检查结果：目录是否存在、agent 是否写入、配置是否通过校验。
9. 如果发现客户本地原有配置和仓库定义冲突，不要擅自覆盖关键用户配置，先明确指出冲突点。
```

## 导入成功标准

不是只看页面。

成功标准是：

1. `~/.openclaw/domains/creator-outreach-opc` 存在
2. 里面有：
   - `agents/laicai`
   - `agents/facai`
   - `workspace/registry`
   - `workspace/evidence`
   - `workspace/inbox`
3. `~/.openclaw/openclaw.json` 里存在：
   - `main`
   - `wangcai`
   - `laicai`
   - `facai`
4. `openclaw config validate` 通过

## 备注

- 仓库里的 `import.ps1` / `import.sh` 仍可保留作为辅助入口
- 但客户交付时，优先采用 **Codex 按仓库权威文件执行本地导入** 的方式
- 这样更可控，也更容易发现和处理客户现场配置冲突
