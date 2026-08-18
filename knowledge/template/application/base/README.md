---
# 应用四类固定目录契约标准源：Base
# 本文件是 application 下 base/ 目录 README 的唯一正文标准源。
# 所有 knowledge/applications/{appCode}/base/README.md 的正文必须与此完全一致。
# 本文件不绑定任何 appCode，不允许 application 自行改写目录职责。
id: KB-INFRA-TEMPLATE-APP-BASE-README
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- infrastructure
- template
- contract
- base
anchors:
- GLOBAL:BASE-CONTRACT
---

# Base

## 目录定位

`base/` 是应用的基础事实与代码定位层。

本目录用于记录当前应用中已经能够通过代码、配置、数据库或其他可靠来源验证的基础事实，并为开发者和 Coding Agent 提供准确、快速的代码与资源定位入口。

Base 主要回答：

> 当前真实事实是什么，以及对应代码或资源在哪里？

## 应包含的内容

本目录适合记录：

- 模块及子模块索引
- API、Controller 等接口入口
- DTO、VO、DO、Model 等数据模型定位
- 数据库表、字段及相关数据结构定位
- 配置项及配置文件入口
- MQ、Job、定时任务、异步处理入口
- 权限相关代码入口
- 核心 Service、Repository、Mapper 等代码定位
- 关键目录和文件位置
- 当前项目已经确认存在的其他基础事实
- 面向代码检索和事实定位的索引型知识

内容应尽量提供可以直接验证和定位的事实。

## 不应包含的内容

以下内容不属于 Base：

- 功能能力、用户能力和主要业务流程，应进入 `feature/`
- 必须成立的业务规则、权限规则、状态约束和数据边界，应进入 `rule/`
- 架构原理、框架机制、事务、缓存、MQ、异常处理等技术实现知识，应进入 `tech/`
- 尚未验证的推测或规划内容，不得作为 Base 事实记录

Base 不负责解释“为什么这样设计”，也不负责展开完整技术方案。

## 维护规则

- 只记录能够被可靠证据验证的当前事实
- 优先提供明确、可直接使用的代码或资源定位入口
- 不把推测、历史印象或规划内容写成当前事实
- 当代码、配置、数据库或相关事实发生变化时，应同步更新对应 Base 知识
- 避免在 Base 中重复 Feature、Rule 或 Tech 已经承担的内容
- Base 应保持事实导向和定位导向，避免扩展成大篇幅设计说明
