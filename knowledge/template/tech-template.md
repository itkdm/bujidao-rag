---
# ==================== 必填字段 ====================
id: KB-TECH-{DOMAIN}-{APP}-{TOPIC}
type: tech
scope: {cross-app/appCode}

# 业务归属
domain: {domain}
application: {appCode}
appType: {前端应用/后端应用}

# 技术分类
techArea: {architecture/framework/api-integration/data-transaction/async-job/error-observability/security-permission/build-env/testing-quality/troubleshooting}
topic: {topicCode}

# 状态管理
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
  - APPLICATION:{appCode}
  - TECH_AREA:{techArea}
  - TECH_TOPIC:{topicCode}
---

# {技术主题名称}

## AI 使用摘要

- 适用场景：{什么任务需要读取本文}
- 关键入口：{核心类/配置/目录/命令/脚本}
- 关键规则：{本文最重要的约束，最多三条}
- 关联知识：{相关 feature/rule/base/tech 文档}
- 使用前必须核对：{代码路径、配置、依赖版本、环境变量、上游变更等}

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | {相关代码路径} | {代码核对说明} |
| doc | {相关文档路径} | {文档来源说明} |
| human | {确认人/时间} | {人工确认说明} |

## 适用范围

说明本文约束适用于哪些模块、场景、接口、任务类型或运行环境。

## 不适用范围

说明本文不覆盖什么，避免 AI 或开发者把约束外推到错误场景。

## 核心结论

用简短条目写清楚本文的稳定结论。结论必须能被证据支持。

## 背景与约束

说明为什么存在这个技术约束，包括上游框架限制、历史原因、环境限制、性能/安全/一致性要求等。

## 标准做法

描述推荐实现方式。必要时给出最小代码片段、配置片段或目录示例。

## 禁止或谨慎做法

列出容易引入缺陷、破坏一致性、绕过框架能力或影响后续维护的写法。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| {对象} | `{路径或名称}` | {用途说明} |

## 变更影响与检查清单

- [ ] {修改此主题相关代码前必须检查的事项}
- [ ] {修改后必须验证的事项}

## 常见问题与踩坑

记录稳定、可复现、对后续实现有帮助的问题。未经确认的推断先进入 `candidate/`。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| {问题} | 待确认 | {影响说明} |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | YYYY-MM-DD | 初始版本 | 布吉岛 |
