---
id: KB-APP-RUOYI-VUE-PRO
type: application
scope: app
appCode: ruoyi-vue-pro
status: DRAFT
owner: bujidao
maintainers:
- bujidao
version: 5
updatedAt: 2026-08-23
verifiedAt: 2026-08-23
confidence: high
stability: evolving
evidence:
- type: code
  ref: ruoyi-vue-pro/
- type: code
  ref: ruoyi-vue-pro/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md
tags:
- backend
- java17
- spring-boot
- ruoyi-vue-pro
- yudao
anchors:
- APP:RUOYI-VUE-PRO
---

# ruoyi-vue-pro 单体后端基线示例

## AI 使用摘要

- 适用场景：了解本模板仓库选取的芋道单体后端形态、当前版本、启用模块和代码边界时
- 关键入口：`ruoyi-vue-pro/pom.xml`、`ruoyi-vue-pro/yudao-server/pom.xml`、`YudaoServerApplication.java`
- 关键规则：目录存在不等于模块已启用；上游提供的模块能力不等于目标项目已经采用的能力
- 关联知识：[INDEX.md](./INDEX.md)
- 初始化要求：复制本体系到目标项目时，必须按目标工作区重新识别后端形态、版本和模块，不得沿用本文件结论

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | Java 版本、工程版本和根工程模块 |
| code | `ruoyi-vue-pro/yudao-server/pom.xml` | 启动模块实际装配的业务模块 |
| code | `YudaoServerApplication.java` | 单体后端启动入口 |
| doc | `knowledge/reference/.../09.项目结构.md` | 芋道官方项目结构说明 |

## 概述

`ruoyi-vue-pro/` 是本模板仓库采用的芋道单体后端示例，来源形态为 `master-jdk17`。它用于展示如何为一个真实应用建立 application、base、feature、rule、tech 五类知识入口。

本文只记录当前示例工作区可从代码验证的技术事实，不定义任何目标用户的产品、行业或业务范围。目标项目可能使用芋道单体版、微服务版，也可能完全不使用芋道；初始化时必须根据真实代码重新生成应用知识。

## 基本信息

| 属性 | 当前示例值 |
| --- | --- |
| 应用编码 | `ruoyi-vue-pro` |
| 工程形态 | Maven 多模块单体应用 |
| 上游系列 | 芋道 `ruoyi-vue-pro` |
| 基线分支 | `master-jdk17` |
| 工程版本 | `2026.07-SNAPSHOT` |
| Java 版本 | 17 |
| 启动模块 | `yudao-server` |
| 技术栈 | Java 17 / Spring Boot 3.5.15 / Maven |

## 当前模块状态

### 参与聚合构建与启动装配

根据当前 `ruoyi-vue-pro/pom.xml` 与 `yudao-server/pom.xml`，以下模块参与根工程聚合；其中 `system`、`infra` 也被启动模块依赖：

| 模块 | 职责 |
| --- | --- |
| `yudao-dependencies` | 依赖版本统一管理 |
| `yudao-framework` | 通用框架与 Starter |
| `yudao-server` | 应用启动和模块装配 |
| `yudao-module-system` | 系统级基础能力模块 |
| `yudao-module-infra` | 基础设施模块 |

### 目录存在但未参与当前聚合或装配

以下模块目录在上游全量基线中存在，但当前根 `pom.xml` 对应声明被注释：

| 模块组 | 当前状态 |
| --- | --- |
| `member`、`bpm`、`report`、`mp`、`pay`、`mall` | 未参与当前聚合或启动装配 |
| `crm`、`erp`、`iot`、`mes`、`wms`、`hrm`、`fms` | 未参与当前聚合或启动装配 |
| `im`、`ai` | 未参与当前聚合或启动装配 |

这些条目只说明上游目录和当前构建状态，不表达目标项目应该启用哪些模块。

## 系统边界

### 当前示例边界

```text
[yudao-ui-admin-vue3]
          |
          v
[ruoyi-vue-pro / yudao-server]
          |
          +--> [system]
          +--> [infra]
          |
          v
[数据库 / Redis / 外部基础设施]
```

### 初始化后的边界

目标项目初始化时，应根据实际代码重新确认：

- 使用单体版还是微服务版
- 实际启动入口和部署单元
- 当前参与构建及运行的模块
- 实际前端、客户端或外部系统调用方
- 数据库、缓存、消息队列和外部服务依赖

## 核心模块

| 模块 | 当前示例职责 | 初始化时必须核对 |
| --- | --- | --- |
| `yudao-server` | 启动与装配 | 实际依赖和 Profile |
| `yudao-framework` | 框架层 | Starter、扩展点和版本 |
| `yudao-module-system` | 参与聚合且进入启动装配 | 是否保留、裁剪或扩展 |
| `yudao-module-infra` | 参与聚合且进入启动装配 | 是否保留、裁剪或扩展 |
| 其他 `yudao-module-*` | 当前未参与聚合或装配 | 目标项目是否真实采用 |

## 待初始化项

| 项目 | 为什么不能从模板继承 |
| --- | --- |
| 芋道单体版或微服务版 | 决定应用边界、部署单元和知识目录 |
| 上游版本和接入提交 | 不同用户可能采用不同分支或版本 |
| 启用模块集合 | 根工程、启动模块和配置可能不同 |
| 前端形态 | 芋道存在多个管理后台和移动端实现 |
| 数据与基础设施 | 数据库、缓存、MQ 只能以目标环境为准 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 2 | 2026-08-09 | 区分当前事实、目标定位与待确认边界 | 布吉岛 |
| 3 | 2026-08-09 | 校准知识 ID | 布吉岛 |
| 5 | 2026-08-23 | 移除具体业务定位，改为芋道单体后端通用示例 | Codex |
