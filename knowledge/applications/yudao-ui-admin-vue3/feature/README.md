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

# feature/

## 目录定位

`feature/` 用于记录应用当前已经确认存在的功能能力、功能边界和主要业务流程。核心问题：「这个应用现在能做什么？」

本契约与具体 appCode 无关，所有应用目录下的 `feature/` 共享同一套职责定义。

## 应包含的内容

- 已确认存在的功能能力
- 用户或业务可感知的能力
- 主要业务流程
- 功能之间的关系
- 功能边界
- 当前应用真正已经具备的业务能力

## 不应包含的内容

- API、DTO、数据库表、代码位置：应放入 `base/`。
- 必须遵守的业务规则、权限规则、状态约束：应放入 `rule/`。
- Controller、事务、缓存、MQ 等技术实现方式：应放入 `tech/`。
- 尚未实现或仅规划中的能力，不得当作当前 feature。

## 维护规则

- 只记录已经确认存在的功能。
- 不因为上游项目拥有某功能，就认定当前 application 已经拥有。
- 规划中的功能必须与当前事实区分。
- feature 描述「能力和流程」，不是代码实现细节。
