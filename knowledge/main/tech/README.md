---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-MAIN-TECH-README
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
- global
anchors:
- GLOBAL:MAIN-TECH-README
---

# tech/

## 目录定位

`main/tech/` 存放**跨应用、跨系统、跨业务线**统一遵守的技术知识与技术约束，是团队共用的「技术层面如何构建」约束来源。

## 应包含的内容

- 跨应用共享的技术约束（框架使用约定、关键技术选型约束）。
- 跨应用统一的工程规范（分支策略、提交规范、代码评审、发布流程等）。
- 多应用都要遵守的全局基础设施约定。

## 不应包含的内容

- 仅影响单个应用的应用级技术约束：应放入对应 `applications/{appCode}/tech/`。
- 基础事实与配置：应放入对应应用的 `base/`。
- 功能能力与业务流程：应放入对应应用的 `feature/`。
- 应用内业务规则：应放入对应应用的 `rule/`。

## 维护规则

- 只有「跨应用强制统一」的技术约束才放入本目录，单一应用相关的技术内容不放入。
- 技术约束变化后，必须回到真实代码 / 部署核对并更新 `verifiedAt`。
- 易变内容只提供定位入口，真正改动前回到当前仓库核对真实实现。
