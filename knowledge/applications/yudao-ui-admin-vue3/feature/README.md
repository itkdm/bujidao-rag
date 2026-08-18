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

`feature/` 用于记录应用当前已经确认存在的功能能力、功能边界和主要业务流程。

Feature 主要回答：

> 这个应用现在能做什么？

这里描述的是当前应用真正具备的能力，而不是上游项目可能提供的能力、未来计划实现的功能或具体代码实现方式。

## 应包含的内容

本目录适合记录：

- 当前已经确认存在的功能能力
- 用户或业务能够感知的应用能力
- 主要业务流程
- 功能之间的关系
- 功能入口和功能边界
- 某项能力当前支持和不支持的范围
- 已经落地并能够被验证的业务能力

Feature 应重点帮助开发者和 Coding Agent 理解：

> 当前应用具有哪些真实能力，以及这些能力之间如何协作。

## 不应包含的内容

以下内容不属于 Feature：

- API、DTO、Model、数据库表、代码路径等事实定位，应进入 `base/`
- 必须满足的业务规则、权限规则、状态约束和数据边界，应进入 `rule/`
- Controller、Service、事务、缓存、MQ、异常处理等技术实现知识，应进入 `tech/`
- 尚未实现、仅处于规划阶段或只是上游项目存在的功能，不得描述为当前 Feature

Feature 不负责展开底层代码实现。

## 维护规则

- 只记录已经确认存在的当前功能能力
- 不因为上游框架、上游仓库或其他应用存在某项功能，就默认当前应用已经拥有该能力
- 规划中的能力必须与当前已经实现的能力严格区分
- Feature 重点描述能力、边界和流程，不展开具体工程实现
- 功能发生实质变化时，应同步更新相关 Feature 知识
- 避免与 Base、Rule、Tech 重复记录同一层面的信息
