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

# tech/

## 目录定位

`tech/` 是应用知识目录下存放**技术约束与部署架构**的目录，描述系统「技术层面如何构建与运行」。

本契约与具体 appCode 无关，所有应用目录下的 `tech/` 共享同一套职责定义。

## 应包含的内容

- 应用级技术约束（框架使用约定、关键技术选型约束）。
- 部署架构与运行拓扑。
- 需要团队遵守、与应用强相关的技术约定。

## 不应包含的内容

- 基础事实与配置项：应放入 `base/`。
- 功能能力与业务流程：应放入 `feature/`。
- 业务规则与研发规范：应放入 `rule/`。
- 跨应用共享的全局技术约束：应放入 `main/tech/`。

## 维护规则

- 只记录当前已确认的技术约束与架构事实，不把规划当事实。
- 架构或技术约束变化后，必须回到真实代码 / 部署核对并更新 `verifiedAt`。
- 易变内容只提供定位入口，真正改动前回到当前仓库核对真实实现。
