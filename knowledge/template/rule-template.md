---
# ==================== 必填字段（所有 rule 通用） ====================
id: KB-RULE-{DOMAIN}-{APP}-{TOPIC}
type: rule
scope: {cross-app / {appCode}}
status: DRAFT
authorship: {human/ai-assisted/mixed}
owner: {team-name}
maintainers:
  - {userId}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
confidence: medium
stability: evolving

# ==================== 条件字段（仅当 scope != cross-app 时填写） ====================
# 当 scope: cross-app 时，以下字段不填写，也不应填写 global/none/N/A 等伪值。
# 当 scope: {appCode} 时，根据规则实际需要填写，其中 application 应与 scope 对应。
# domain: {domain}
# application: {appCode}
# appType: {前端应用/后端应用}

# 规则分类
ruleArea: {development/collaboration/delivery/security/compliance/boundary/permission/status/data-visibility/config/knowledge-management}
topic: {topicCode}

# 证据
evidence:
  - type: code
    ref: {相关代码路径}
    verifiedAt: YYYY-MM-DD
  - type: doc
    ref: {相关文档路径}
  - type: human
    ref: {确认人/时间}

# 标签与锚点
tags:
  - {tag1}
  - {tag2}
anchors:
  - RULE_AREA:{ruleArea}
  - RULE_TOPIC:{topicCode}
  # 仅当 scope != cross-app 时添加：
  # - APPLICATION:{appCode}
---

# {规则主题名称}

## AI 使用摘要

- 适用场景：{什么任务需要读取本文}
- 关键规则：{本文最重要的规则，最多三条}
- 关联知识：{相关 base/tech/feature/rule 文档，或 main/ 下其他全局知识}
- 使用前必须核对：{规则依赖的代码、配置、文档或人工确认是否变化}

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | {相关代码路径} | {代码核对说明} |
| doc | {相关文档路径} | {文档来源说明} |
| human | {确认人/时间} | {人工确认说明} |

## 规则范围

说明本文规则适用于哪些模块、场景、角色、接口或数据。

## 不适用范围

说明本文规则不覆盖什么，避免外推。

## 规则正文

| 规则 | 内容 | 依据 |
| --- | --- | --- |
| {规则名} | {规则内容} | {证据来源} |

## 例外情况

记录允许偏离规则的场景，以及必须满足的前置条件。

## 违反规则的风险

说明违反规则可能带来的安全、数据、业务、实现或维护风险。

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `domain/base/` | {相关事实入口（仅应用级 rule）} |
| `domain/feature/` | {相关功能流程（仅应用级 rule）} |
| `tech/` | {相关实现约束（仅应用级 rule）} |
| `main/` | {相关全局知识（仅 cross-app rule）} |

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| {问题} | 待确认 | {影响说明} |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | YYYY-MM-DD | 初始版本 | 布吉岛 |
