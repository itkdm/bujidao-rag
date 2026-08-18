---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-YUDAO-TECH-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- contract
anchors:
- GLOBAL:TECH-CONTRACT
---

# Tech

## 目录定位

`tech/` 用于记录当前应用中的技术实现知识、工程实践、技术机制和实现约束。

Tech 主要回答：

> 在当前应用和技术栈中应该怎么实现？

核心语义是：

> How we implement it.

这里关注当前项目实际采用的技术方案和工程实现方式，而不是单纯记录代码位置或业务规则。

## 应包含的内容

本目录适合记录：

- 系统架构与模块边界
- 框架使用方式
- Web 与 API 实现方式
- Controller、Service 等工程实现约定
- 数据访问方式
- ORM、MyBatis 等数据层技术
- 事务机制
- 缓存机制
- MQ 与异步处理
- Job 和定时任务实现
- 权限与安全技术实现
- 异常处理与日志机制
- 构建与本地开发环境
- 测试相关技术实践
- 当前应用中的技术选型及其具体落地方式
- 其他与当前应用工程实现直接相关的技术知识

Tech 不应被缩窄为“部署架构”或“技术约束”。

它承担的是：

> 当前应用完整的技术实现知识。

## 不应包含的内容

以下内容不属于 Tech：

- 功能能力和主要业务流程，应进入 `feature/`
- 必须成立的业务规则、权限规则和状态约束，应进入 `rule/`
- 单纯的 API、Model、数据库表、文件路径等事实定位，应进入 `base/`
- Git Commit、Git Branch、Pull Request 等跨应用通用研发规范，应进入 `main/` 下对应的全局知识目录

Tech 不应把纯业务规则包装成技术知识。

## 维护规则

- 技术知识必须以当前应用真实代码、配置和技术栈为依据
- 重点解释当前项目技术上如何实现，而不是只描述代码在哪里
- 应区分当前真实实现与未来可能采用的方案
- 技术机制或工程约束发生变化后，应及时更新对应 Tech 知识
- 不重复 Base 中已经足够表达的事实定位内容
- 不重复 Rule 中已经定义的业务或系统约束
