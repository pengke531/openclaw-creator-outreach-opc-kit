# Creator Outreach 手动配置总规范

这份文件是当前仓库的 **人工配置权威说明**。

如果客户本地的 OpenClaw 环境已经被之前的错误导入弄乱，不要再继续依赖 `import.ps1`、`import.sh`、自动打包导入。

正确做法是：

1. 在客户本地拉取这个仓库
2. 在客户本地打开 Codex
3. 让 Codex 读取本文件和仓库中的 agent / workspace 文件
4. 由 Codex 或人工按本规范逐项手动配置

## 1. 先说清楚真实需求

客户文件里真正要解决的不是“4 个会聊天的人设”，而是一条可审计的创作者商务流水线：

- 找到符合标准的新创作者
- 做证据充分的筛选
- 做去重和正式建档
- 批准后再外联
- 收到回复后冻结审批
- 在 Day4 / Day8 做 ROI 复盘
- 把优化建议回写到下一轮筛选和话术

所以架构必须服务于流程，而不是服务于角色扮演。

## 2. 哪些客户表述要保留，哪些要修正

保留：

- 1 个主控，3 个执行
- 员工禁止直接对话
- 搜寻、外联、复盘要分开
- 查重和资料库必须是硬要求
- 回复审批必须阻塞

修正：

- `多渠道触达` 和 `目前仅邮箱` 冲突。V1 按 **Email-first** 执行，多渠道只保留为未来扩展。
- `老板无异议默认通过` 只能用于低风险候选名单放行，不能用于回复、报价、条款。
- ROI 不能只写“1.5 倍淘汰，3 倍合格”，必须由客户本地定义清楚公式、时间窗和成本口径。

## 3. 为什么参考 gstack 后，正确架构是 1主3执行

参考 gstack，应该借鉴的是组织方法，不是照抄软件开发角色：

- 一个 orchestrator，不再叠主管层
- 每个阶段只有一个 owner
- 每个阶段都必须产出交付物
- 重型能力放到专职执行层，而不是放在所有人身上
- 主控负责批准、路由、整合，不负责所有细活

因此，creator-outreach 的合理形态是：

```text
老板 / 用户
  ↓
main = Manager
  ├─ wangcai = Discovery & Evidence
  ├─ laicai = Outreach
  └─ facai = ROI Review

系统层：
- workspace/registry
- workspace/evidence
- workspace/inbox
```

这是 **双层架构**，不是三层。  
因为只有：

- 一层主控
- 一层执行

## 4. 正式 Agent 架构

### `main` = Manager

唯一主控，负责：

- 接收老板需求
- 锁定 campaign brief 和 screening rules
- 接收 `wangcai` 的 evidence packet
- 做 dedup 最终裁决
- 写正式 `registry`
- 决定是否放行给 `laicai`
- 审核回复
- 接收 `facai` 的 ROI packet
- 输出最终名单、审批结果、优化策略

绝对不能下放的权限：

- `registry/creators`
- `registry/campaigns`
- `registry/approvals`
- `registry/indexes`
- dedup 最终裁决
- approval 最终裁决

### `wangcai` = Discovery & Evidence Executor

只负责：

- FB / INS creator discovery
- 按规则做硬筛
- page-by-page verification
- 证据采集
- 生成 evidence packet
- 对已入库创作者做动态更新扫描

禁止事项：

- 不得外联
- 不得直接进 `registry`
- 不得做最终 dedup 裁决
- 不得做 approval

### `laicai` = Outreach Executor

只负责：

- 对已批准名单做 Email-first 外联
- 跟进 cadence
- 记录送达、失败、退信、无回复、已回复
- 收到回复后冻结
- 生成 reply packet

禁止事项：

- 不得搜人
- 不得做页面核验
- 不得做 dedup 裁决
- 不得写 `registry`
- 不得自行继续回复
- 不得自行改报价和条款

### `facai` = ROI Review Executor

只负责：

- Day4 review
- Day8 closeout review
- ROI interpretation
- stop-loss suggestion
- optimization packet

禁止事项：

- 不得搜人
- 不得外联
- 不得写 `registry`
- 不得直接改正式 campaign 状态
- 不得直接指挥 `wangcai` 或 `laicai`

## 5. 系统层目录

客户本地 `~/.openclaw/domains/creator-outreach-opc` 下，必须至少有：

```text
agents/
  wangcai/
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
- `wangcai` 写 `workspace/evidence/creators/*`
- `laicai` 只写 `workspace/inbox/outreach-results/*`
- `facai` 只写 `workspace/inbox/roi-results/*`

## 6. OpenClaw 必须达到的配置结果

客户本地 `~/.openclaw/openclaw.json` 最终要达到的核心结果不是“长得一样”，而是下面这些逻辑必须成立。

### 6.1 必须存在的 agent

- `main`
- `wangcai`
- `laicai`
- `facai`

### 6.2 `main` 必须具备的能力

- `read`
- `write`
- `subagents`
- `memory_search`
- `memory_get`
- `memory_store`
- `agents_list`

### 6.3 `main` 的 subagent 限制

`main.subagents.allowAgents` 必须至少包含：

- `wangcai`
- `laicai`
- `facai`

### 6.4 `wangcai` 的能力范围

保留 discovery 和证据采集所需能力：

- `read`
- `write`
- `memory_search`
- `memory_get`
- `memory_store`
- `web_search`
- `web_fetch`
- `browser`

### 6.5 `laicai` 的能力范围

保留窄能力即可：

- `read`
- `write`
- `memory_search`
- `memory_get`
- `memory_store`

### 6.6 `facai` 的能力范围

保留分析所需能力即可：

- `read`
- `write`
- `memory_search`
- `memory_get`
- `memory_store`

## 7. 推荐的 `openclaw.json` 目标片段

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
        "maxChildrenPerAgent": 4,
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
            "agents_list"
          ]
        },
        "subagents": {
          "allowAgents": ["wangcai", "laicai", "facai"],
          "requireAgentId": true
        }
      },
      {
        "id": "wangcai",
        "workspace": "__DOMAIN_ROOT__/agents/wangcai",
        "tools": {
          "profile": "minimal",
          "alsoAllow": [
            "read",
            "write",
            "memory_search",
            "memory_get",
            "memory_store",
            "web_search",
            "web_fetch",
            "browser"
          ]
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
            "memory_store"
          ]
        }
      }
    ]
  }
}
```

## 8. 工作流交付逻辑

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

### 阶段 3：发现与取证

Owner：

- `wangcai`

输出：

- `creator evidence packet`

### 阶段 4：去重与正式建档

Owner：

- `main`

输出：

- `canonical creator record`

### 阶段 5：外联放行

Owner：

- `main`

输出：

- `approved outreach batch`

### 阶段 6：外联执行

Owner：

- `laicai`

输出：

- `workspace/inbox/outreach-results/*`

### 阶段 7：回复审批

Owner：

- `main`

输出：

- `registry/approvals/*`

### 阶段 8：ROI 复盘

Owner：

- `facai`

输出：

- `workspace/inbox/roi-results/*`

### 阶段 9：策略回写

Owner：

- `main`

输出：

- 更新后的规则、状态、结论

## 9. 状态机

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

## 10. 手动配置时应该读取哪些仓库文件

客户本地 Codex 或人工在手动配置时，优先读取这些文件：

- `openclaw.json`
- `workspace/AGENTS.md`
- `workspace/MEMORY.md`
- `workspace/knowledge/creator-memory-and-state-model.md`
- `agents/wangcai/*`
- `agents/laicai/*`
- `agents/facai/*`
- `workspace/schemas/creator.schema.json`
- `workspace/schemas/campaign.schema.json`
- `workspace/schemas/approval.schema.json`

## 11. 手动配置检查清单

手动配置完成后，至少检查：

1. `main` 是否真的是唯一主控
2. `main` 是否只允许调度 `wangcai`、`laicai`、`facai`
3. `wangcai` 是否承担 discovery 和证据采集
4. `laicai` 是否没有正式库写权限
5. `facai` 是否没有正式库写权限
6. `workspace/registry`、`workspace/evidence`、`workspace/inbox` 是否完整
7. 回复事件是否会在 `laicai` 处冻结
8. `openclaw config validate` 是否通过

## 12. 给客户本地 Codex 的最短指令

如果你只想给客户本地 Codex 一段最短要求，就用这段：

```text
请不要使用仓库里的自动导入脚本，也不要自行发明新的 agent 层级。

请只根据当前仓库中的以下文件，手动整理并配置这套 creator-outreach 架构：
- MANUAL_CONFIGURATION_SPEC.md
- openclaw.json
- workspace/AGENTS.md
- workspace/MEMORY.md
- workspace/knowledge/creator-memory-and-state-model.md
- agents/wangcai/*
- agents/laicai/*
- agents/facai/*
- workspace/schemas/*

目标是：
1. 将客户本地 creator-outreach 架构整理成双层结构：main=Manager，wangcai=侦察执行，laicai=外联执行，facai=复盘执行。
2. 保证只有 main 是主控，其他三个都是执行层。
3. 保证 discovery 与 hard evidence 归 wangcai，外联归 laicai，ROI 归 facai。
4. 保证 registry 正式写入只属于 main。
5. 按本规范手动检查并修正客户本地 openclaw 配置、目录结构、职责边界和状态流转。
6. 完成后输出：当前 agent 拓扑、关键权限、目录结构、仍存在的冲突点。
```
