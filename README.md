# OpenClaw Creator Outreach OPC Kit

给已经安装好 OpenClaw 的用户使用。

这套仓库现在可以直接提供一条可安装、可运行的 Instagram Nepal creator pipeline：

- 安装 domain pack 到现有 OpenClaw
- 自动挂载 shared skill
- 自动提供 `/workking` 口令入口
- 自动安装 recurring cron
- 支持手动跑批
- 支持最终 3 列名单导出

## 当前正式架构

- `main` = Manager，唯一主控
- `wangcai` = Discovery 与 Evidence 执行
- `laicai` = Outreach 执行
- `facai` = ROI 复盘执行

系统层不是 agent：

- `workspace/registry`
- `workspace/evidence`
- `workspace/inbox`

## Instagram Nepal 现成入口

安装：

- Windows: `powershell -ExecutionPolicy Bypass -File .\install-creator-outreach.ps1`
- Bash: `./install-creator-outreach.sh`

手动跑一轮：

- Windows: `powershell -ExecutionPolicy Bypass -File .\run-instagram-nepal-batch.ps1`
- Bash: `./run-instagram-nepal-batch.sh`

安装定时批处理：

- Windows: `powershell -ExecutionPolicy Bypass -File .\install-instagram-nepal-cron.ps1`
- Bash: `./install-instagram-nepal-cron.sh`

导出最终名单：

- Windows: `powershell -ExecutionPolicy Bypass -File .\export-instagram-nepal-submissions.ps1 -Format markdown -OutputPath "$HOME\Desktop\instagram-nepal-submissions.md"`

聊天内直接启动：

- 新开一个会话后输入：`/workking`
- 查看状态：`/workking status`
- 手动停止：`/workking stop`

## 当前默认策略

- 平台：Instagram only
- 地区：Nepal only
- 逻辑批次：24
- 内部微批次：8
- 默认定时：每 12 小时一轮
- 单轮超时：15 分钟
- 无新增停机：30 分钟
- 爬虫偏好：每次启动按顺序轮换
- 证据不足：`EVIDENCE_GAP`
- 未完全达标：不得入库
- 重复账号：只更新，不重复提交

## 关键路径

- 安装和运行说明：`workspace/docs/runbooks/install-and-run-instagram-nepal.md`
- Skill：`workspace/skills/shared/instagram-nepal-creator-pipeline/SKILL.md`
- 口令入口 Skill：`workspace/skills/shared/workking/SKILL.md`
- 批处理与导出入口：`workspace/scripts/instagram_ops.py`
- Runtime 状态机：`workspace/scripts/instagram_runtime.py`
- 注册与去重 helper：`workspace/scripts/instagram_registry_ops.py`
- 手动配置总规范：`MANUAL_CONFIGURATION_SPEC.md`

## 仓库地址

`https://github.com/pengke531/openclaw-creator-outreach-opc-kit`
