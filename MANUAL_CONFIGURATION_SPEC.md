# Creator Outreach 手动配置总规范

这份文件是当前仓库的 **人工配置权威说明**。

如果客户本地的 OpenClaw 环境已经被之前的错误导入弄乱，不要再继续依赖 `import.ps1`、`import.sh`、自动打包导入。

正确做法是：

1. 在客户本地拉取这个仓库
2. 在客户本地打开 Codex
3. 让 Codex 读取本文件和仓库中的 agent / workspace 文件
4. 由 Codex 或人工按本规范逐项手动配置

---

## 1. 目标架构

最终架构必须是 **双层**，不是三层。

```text
老板 / 用户
  ↓
main = 旺财
  ├─ laicai = 来财
  └─ facai = 发财

系统层：
- workspace/registry
- workspace/evidence
- workspace/inbox
```

硬规则：

- `main` 是唯一主控
- 不再存在中间“主管 agent”
- `laicai` 和 `facai` 都只能被 `main` 调度
- `laicai` 和 `facai` 不能互相调度
- 正式资料库只能由 `main` 写入

---

## 2. Agent 职责边界

### `main` = 旺财

唯一主控，负责：

- 接收老板需求
- 锁定 campaign brief 和 screening rules
- 搜索候选 creator
- 做 Facebook / 主页逐页核验
- 做证据收集
- 做去重裁决
- 写正式 `registry`
- 决定是否放行外联
- 审核回复
- 回收来财和发财的结果
- 输出最终名单和策略调整

绝对不能下放的权限：

- `registry/creators`
- `registry/campaigns`
- `registry/approvals`
- `registry/indexes`
- Facebook 硬核验
- dedup 最终裁决
- approval 最终裁决

### `laicai` = 来财

窄执行 agent，只负责：

- 对已经批准的名单做外联
- 跟进 cadence
- 记录送达 / 失败 / 无回复 / 已回复
- 收到回复后冻结
- 输出 reply packet 到 `workspace/inbox/outreach-results`

禁止事项：

- 不得搜人
- 不得做 Facebook 核验
- 不得做 dedup 裁决
- 不得写 `workspace/registry`
- 不得在收到回复后自行继续推进
- 不得自行改价格、条款、合作条件

### `facai` = 发财

窄执行 agent，只负责：

- Day4 review
- Day8 closeout review
- ROI interpretation
- stop-loss suggestion
- optimization packet

输出位置：

- `workspace/inbox/roi-results`

禁止事项：

- 不得搜人
- 不得做外联
- 不得写 `workspace/registry`
- 不得直接改 campaign 正式状态
- 不得直接指挥 `laicai`

---

## 3. 系统层目录

客户本地 `~/.openclaw/domains/creator-outreach-opc` 下，必须至少有：

```text
agents/
  laicai/
  facai/

workspace/
  AGENTS.md
  MEMORY.md
  registry/
    creators/
    campaigns/
    approvals/
    metrics/
    indexes/
  evidence/
    creators/
    campaigns/
  inbox/
    outreach-results/
    roi-results/
  schemas/
  templates/
  docs/
  knowledge/
```

写权限规则：

- `main` 可写 `workspace/registry/*`
- `main` 可写 `workspace/evidence/*`
- `laicai` 只写 `workspace/inbox/outreach-results/*`
- `facai` 只写 `workspace/inbox/roi-results/*`

---

## 4. OpenClaw 必须达到的配置结果

客户本地 `~/.openclaw/openclaw.json` 最终要达到的核心结果不是“长得一样”，而是下面这些逻辑必须成立。

### 4.1 必须存在的 agent

- `main`
- `laicai`
- `facai`

### 4.2 `main` 必须具备的能力

- `read`
- `write`
- `subagents`
- `memory_search`
- `memory_get`
- `memory_store`
- `agents_list`
- `web_search`
- `web_fetch`
- `browser`

### 4.3 `main` 的 subagent 限制

`main.subagents.allowAgents` 必须至少包含：

- `laicai`
- `facai`

### 4.4 `laicai` 的能力范围

保留窄能力即可：

- `read`
- `write`
- `memory_search`
- `memory_get`
- `memory_store`

不要默认给：

- `browser`
- 强搜索核验能力
- 再调度其他 agent 的能力

### 4.5 `facai` 的能力范围

保留分析所需能力即可：

- `read`
- `write`
- `memory_search`
- `memory_get`
- `memory_store`
- `web_search`
- `web_fetch`

不要默认给：

- `browser`
- 搜人主权限
- 审批写权限

---

## 5. 推荐的 `openclaw.json` 目标片段

下面是目标形态，客户本地可以按这个合并，而不是机械覆盖。

```json
{
  "agents": {
    "defaults": {
      "workspace": "__DOMAIN_ROOT__/workspace",
      "memorySearch": {
        "enabled": true
      },
      "subagents": {
        "maxChildrenPerAgent": 3,
        "maxSpawnDepth": 2,
        "runTimeoutSeconds": 900,
        "archiveAfterMinutes": 60,
        "requireAgentId": true
      }
    },
    "list": [
      {
        "id": "main",
        "workspace": "__DOMAIN_ROOT__/workspace",
        "tools": {
          "profile": "messaging",
          "alsoAllow": [
            "read",
            "write",
            "subagents",
            "memory_search",
            "memory_get",
            "memory_store",
            "agents_list",
            "web_search",
            "web_fetch",
            "browser"
          ]
        },
        "subagents": {
          "allowAgents": ["laicai", "facai"],
          "requireAgentId": true
        }
      },
      {
        "id": "laicai",
        "workspace": "__DOMAIN_ROOT__/agents/laicai",
        "tools": {
          "profile": "minimal",
          "alsoAllow": [
            "read",
            "write",
            "memory_search",
            "memory_get",
            "memory_store"
          ]
        }
      },
      {
        "id": "facai",
        "workspace": "__DOMAIN_ROOT__/agents/facai",
        "tools": {
          "profile": "minimal",
          "alsoAllow": [
            "read",
            "write",
            "memory_search",
            "memory_get",
            "memory_store",
            "web_search",
            "web_fetch"
          ]
        }
      }
    ]
  }
}
```

注意：

- 如果客户本地已有 `main`，目标不是盲删，而是把它重构成这里定义的旺财主控形态
- 如果客户本地已有别的 agent，不要自动删掉，但不要让它们破坏这套 creator 场景的主控关系

---

## 6. 工作流交付逻辑

### 阶段 1：需求 intake

Owner：

- `main`

输出：

- `campaign brief`

### 阶段 2：规则锁定

Owner：

- `main`

输出：

- `screening rules`

### 阶段 3：取证与去重

Owner：

- `main`

输出：

- `creator evidence packet`
- `canonical creator record`

### 阶段 4：放行外联

Owner：

- `main`

输出：

- `approved outreach batch`

### 阶段 5：外联执行

Owner：

- `laicai`

输出：

- `workspace/inbox/outreach-results/*`

### 阶段 6：回复审批

Owner：

- `main`

输出：

- `registry/approvals/*`

### 阶段 7：ROI 复盘

Owner：

- `facai`

输出：

- `workspace/inbox/roi-results/*`

### 阶段 8：策略回写

Owner：

- `main`

输出：

- 更新后的规则、状态、结论

---

## 7. 状态机

### Creator 状态机

```text
discovered
-> evidence_collecting
-> evidence_gap | screened_fail | screened_pass
-> dedup_rejected | registered
-> approved_for_outreach
-> outreach_in_progress
-> reply_received
-> reply_pending_approval
-> negotiation_active
-> day4_review
-> day4_stoploss | day8_review
-> qualified | low_quality | excluded
-> closed
```

### Campaign 状态机

```text
brief_created
-> rules_locked
-> screening_active
-> outreach_ready
-> outreach_active
-> reply_handling
-> mid_review
-> closeout_review
-> optimized
-> closed
```

---

## 8. 手动配置时应该读取哪些仓库文件

客户本地 Codex 或人工在手动配置时，优先读取这些文件：

- `openclaw.json`
- `workspace/AGENTS.md`
- `workspace/MEMORY.md`
- `workspace/knowledge/creator-memory-and-state-model.md`
- `agents/laicai/AGENTS.md`
- `agents/facai/AGENTS.md`
- `workspace/schemas/creator.schema.json`
- `workspace/schemas/campaign.schema.json`
- `workspace/schemas/approval.schema.json`

如果只读一部分，很容易再次出现：

- 层级错误
- 权限边界错误
- 资料库写入错误
- 工作流断裂

---

## 9. 手动配置检查清单

手动配置完成后，至少检查：

1. `main` 是否真的是旺财主控
2. `main` 是否只允许调度 `laicai` 和 `facai`
3. `laicai` 是否没有正式库写权限
4. `facai` 是否没有正式库写权限
5. `workspace/registry`、`workspace/evidence`、`workspace/inbox` 是否完整
6. Facebook 取证是否由 `main` 负责
7. 回复事件是否会在 `laicai` 处冻结
8. `openclaw config validate` 是否通过

---

## 10. 给客户本地 Codex 的最短指令

如果你只想给客户本地 Codex 一段最短要求，就用这段：

```text
请不要使用仓库里的自动导入脚本，也不要自行发明新的 agent 层级。

请只根据当前仓库中的以下文件，手动整理并配置这套 creator-outreach 架构：
- MANUAL_CONFIGURATION_SPEC.md
- openclaw.json
- workspace/AGENTS.md
- workspace/MEMORY.md
- workspace/knowledge/creator-memory-and-state-model.md
- agents/laicai/*
- agents/facai/*
- workspace/schemas/*

目标是：
1. 将客户本地 creator-outreach 架构整理成双层结构：main=旺财，laicai=来财，facai=发财。
2. 删除或绕开错误的中间主管层，不再保留三层编排。
3. 保证 main 是唯一主控，负责正式 registry、evidence、approval。
4. 保证 laicai 和 facai 只是窄执行 agent。
5. 按本规范手动检查并修正客户本地 openclaw 配置、目录结构、职责边界和状态流转。
6. 完成后输出：当前 agent 拓扑、关键权限、目录结构、仍存在的冲突点。
```
