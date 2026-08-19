---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-YUDAO-FEATURE-README
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
- GLOBAL:FEATURE-CONTRACT
---

# Feature

## 目录定位

`feature/` 用于记录应用当前已经确认存在的功能能力、功能边界和主要运行或使用流程。

Feature 主要回答：

> 这个系统现在能做什么？

Feature 不区分"业务功能"还是"系统功能"。只要是当前应用真实提供、能够被用户、业务或其他系统使用或感知的能力，都可以属于 Feature。

## 应包含的内容

本目录适合记录：

- 当前已经确认存在的功能能力
- 业务功能，例如订单、商品、知识库等能力
- 系统级功能，例如登录、认证、权限管理、文件上传、消息通知等能力
- 功能的主要使用或运行流程
- 功能之间的关系
- 功能入口和功能边界
- 当前支持和不支持的范围

## 不应包含的内容

以下内容不属于 Feature：

- API、DTO、Model、数据库表、代码路径等事实定位，应进入 `base/`
- 必须满足的业务规则、权限规则、状态约束和数据边界，应进入 `rule/`
- 框架、Controller、Service、JWT、缓存、MQ、事务等具体技术实现，应进入 `tech/`
- 尚未实现或仅存在于上游项目中的能力，不得描述为当前 Feature

Feature 描述"系统具备什么能力"，不展开"技术上如何实现"。

## 维护规则

- 只记录已经确认存在的当前功能能力
- 不区分业务功能和系统功能，以"系统是否真实提供该能力"为判断标准
- 不因为上游框架存在某能力，就默认当前应用已经拥有
- 规划能力必须与当前已实现能力严格区分
- 重点描述能力、流程和边界，不展开技术实现
- 避免与 Base、Rule、Tech 重复
