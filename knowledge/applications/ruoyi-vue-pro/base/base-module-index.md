---
id: KB-BASE-RUOYI-VUE-PRO-MODULE
type: base
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
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md
- type: human
  ref: 布吉岛确认当前尚未进行夸友业务改造，2026-08-09
tags:
- backend
- module
- package
anchors:
- APP:RUOYI-VUE-PRO
- BASE:MODULE
---

# 模块与包结构索引

## AI 使用摘要

- 适用场景：定位后端模块、判断模块是否启用、查找标准包结构时
- 关键入口：`ruoyi-vue-pro/pom.xml`
- 关键事实：当前启用模块只有 `dependencies/framework/server/system/infra`；未启用模块目录仍存在；启动扫描依赖 `yudao.info.base-package`
- 关联知识：[tech-architecture-module-boundary.md](../../tech/tech-architecture-module-boundary.md)
- 使用前必须核对：根 `pom.xml`、`yudao-server/pom.xml`、启动类扫描范围

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | 当前 Maven 模块启用状态 |
| code | `YudaoServerApplication.java` | 启动扫描范围 |
| code | `yudao-module-system/src/main/java/.../system/` | 当前启用模块的标准包结构 |
| doc | `09.项目结构.md` | 官方模块结构说明 |
| human | 布吉岛确认，2026-08-09 | 当前尚未进行夸友业务改造 |

## 索引范围

本文索引 Maven 模块、启动入口、当前启用状态、标准包结构和核心路径。

## 不收录范围

本文不解释模块边界为什么这样设计；相关实现约束见 `tech/tech-architecture-module-boundary.md`。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| 根工程 | `ruoyi-vue-pro/pom.xml` | Maven | 判断模块启用状态 |
| 依赖模块 | `yudao-dependencies` | Maven module | 已启用，依赖版本管理 |
| 框架模块 | `yudao-framework` | Maven module | 已启用，通用 starter 和框架能力 |
| 启动模块 | `yudao-server` | Maven module | 已启用，后端启动入口 |
| 系统模块 | `yudao-module-system` | Maven module | 已启用，用户、权限、系统基础能力 |
| 基建模块 | `yudao-module-infra` | Maven module | 已启用，基础设施、任务、代码生成等 |
| 业务模块目录 | `yudao-module-mall/member/pay/...` | 目录 | 目录存在，但根 `pom.xml` 当前注释未启用 |
| 启动类 | `yudao-server/.../YudaoServerApplication.java` | Java class | Spring Boot 启动入口 |

## 命名与定位规则

- Maven 业务模块命名为 `yudao-module-{module}`。
- Java 包路径遵循 `cn.iocoder.yudao.module.{module}`。
- 模块内常见包：`controller`、`service`、`dal`、`api`、`mq`、`job`、`enums`。
- 管理后台 Controller 位于 `controller.admin`。
- 用户端/小程序 Controller 位于 `controller.app`。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `ruoyi-vue-pro/pom.xml` | 根模块启用状态 | 当前判断模块是否参与构建的第一入口 |
| `yudao-server/src/main/java/.../YudaoServerApplication.java` | 启动入口 | 使用 `${yudao.info.base-package}.server` 和 `.module` 扫描 |
| `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/` | 系统模块源码 | 当前标准包结构参考 |
| `yudao-module-infra/src/main/java/cn/iocoder/yudao/module/infra/` | 基建模块源码 | 代码生成、任务、配置等入口 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | 模块边界和启用约束见 `tech-architecture-module-boundary.md` |
| `feature/` | 后续夸友业务流程落地后，应反向标记所属模块 |
| `rule/` | 业务角色和权限规则确定后，会影响模块划分 |

## 变更影响

模块启用状态变化会影响 Maven 构建、Spring 扫描、数据库脚本、菜单权限、MQ/Job 是否启动，以及 AI 后续代码定位。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友是否新增独立业务模块 | 待确认 | 影响后续包名和模块边界 |
| 是否启用上游 `mall/member/pay` | 待确认 | 影响商城、用户、支付能力来源 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |