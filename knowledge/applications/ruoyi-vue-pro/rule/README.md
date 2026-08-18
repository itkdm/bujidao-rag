---
id: KB-INFRA-RUOYI-RULE-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- infrastructure
- readme
anchors:
- GLOBAL:RUOYI-RULE-README
---

# rule/

## 本目录负责什么

`rule/` 回答：**做这件事必须满足什么规则和边界？**

沉淀应用级的规则与约束，核心表达 **What must be true**。

## 什么内容应该放这里

- 业务规则
- 权限规则
- 状态约束
- 数据边界
- 安全边界
- 必须遵守的应用级约束

## 什么内容不应该放这里，以及应该去哪里

- 具体代码对象、API、表在哪里 → `base/`
- 如何实现、框架用法、工程约定 → `tech/`
- 业务流程或功能能力描述 → `feature/`
- 技术实现方式本身 → `rule/` 只定义规则，不展开实现

## 新增本类知识时需要遵守的最基本归属原则

只定义必须为真（must be true）的规则与边界；不写事实入口，不展开实现方案，不把业务流程当规则。
