---
id: KB-RULE-RUOYI-VUE-PRO-BACKEND-BASELINE
type: rule
scope: app
appCode: ruoyi-vue-pro
status: DRAFT
owner: bujidao
maintainers:
- bujidao
version: 2
updatedAt: 2026-08-18
verifiedAt: 2026-08-09
confidence: high
stability: evolving
evidence:
- type: code
  ref: ruoyi-vue-pro/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java
- type: doc
  ref: knowledge/applications/ruoyi-vue-pro/ruoyi-vue-pro.md
- type: doc
  ref: knowledge/applications/ruoyi-vue-pro/domain/base/base-module-index.md
- type: human
  ref: 布吉岛确认当前尚未进行夸友业务改造，2026-08-09
tags:
- backend
- baseline
- boundary
anchors:
- APP:RUOYI-VUE-PRO
- RULE:BACKEND-BASELINE
---

# 后端基线边界规则

## AI 使用摘要

- 适用场景：判断 `ruoyi-vue-pro` 当前能力、评估是否复用上游模块、描述后端现状时
- 关键规则：当前后端仍是上游开源基线；目录存在不等于模块启用；上游模块能力不能直接写成夸友已实现业务能力
- 关联知识：[ruoyi-vue-pro.md](../../ruoyi-vue-pro.md)、[base-module-index.md](../base/base-module-index.md)、[tech-architecture-module-boundary.md](../../tech/tech-architecture-module-boundary.md)
- 使用前必须核对：根 `pom.xml`、后端应用总览、是否已有夸友业务改造 commit

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | 当前根工程启用模块事实 |
| code | `YudaoServerApplication.java` | 后端启动入口和扫描范围 |
| doc | `ruoyi-vue-pro.md` | 当前后端定位为开源基线 |
| doc | `base-module-index.md` | 当前启用/未启用模块索引 |
| human | 布吉岛确认，2026-08-09 | 当前尚未进行夸友业务改造 |

## 规则范围

适用于所有关于 `ruoyi-vue-pro` 当前状态、模块启用、上游能力复用、夸友后端能力描述的判断。

## 不适用范围

本文不决定未来是否启用 `mall/member/pay` 等模块，也不定义夸友最终业务模块划分。

## 规则正文

| 规则 | 内容 | 依据 |
| --- | --- | --- |
| 基线定位规则 | 当前 `ruoyi-vue-pro/` 只能描述为夸友后端开源基线，不能描述为已完成定制的夸友后端业务系统 | `ruoyi-vue-pro.md`、布吉岛确认 |
| 模块启用规则 | 只有根 `pom.xml` 中未注释的 `<module>` 才视为当前启用模块 | `ruoyi-vue-pro/pom.xml` |
| 目录存在规则 | `mall/member/pay` 等目录存在，不代表这些能力已经启用或已适配夸友业务 | `pom.xml` 当前注释状态 |
| 能力表述规则 | 文档和 AI 回答中不得把上游已有商品、订单、会员、支付等能力直接写成夸友已确认业务能力 | 布吉岛确认、当前未改造状态 |
| 改造前核对规则 | 任何复用上游模块的建议，必须先核对模块启用、数据库脚本、菜单权限、API、数据模型和夸友产品规划 | `base-module-index.md`、`tech-architecture-module-boundary.md` |

## 例外情况

暂无已确认例外。只有当夸友后续提交明确业务改造，并同步更新 application、base、tech 和 rule 知识后，相关模块才能被描述为夸友已适配能力。

## 违反规则的风险

- AI 会把上游示例能力误当成夸友已实现能力，导致错误开发计划。
- 可能错误启用大量未评估模块，引入不需要的表、菜单、任务和依赖。
- 产品文档和技术知识会混淆“当前事实”和“未来目标”，后续追责困难。

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `domain/base/` | 模块启用事实见 `base-module-index.md` |
| `tech/` | 模块边界和启用约束见 `tech-architecture-module-boundary.md` |
| `domain/feature/` | 当前不写夸友业务 feature，避免把未来规划写成现状 |

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友是否新建独立业务模块 | 待确认 | 影响后端业务能力归属 |
| 是否启用上游 `mall/member/pay` | 待确认 | 影响商城、会员、支付能力来源 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |