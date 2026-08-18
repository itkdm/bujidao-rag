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

`feature/` 是应用知识目录下记录**当前已确认的功能能力**与主要业务流程的目录，描述系统「能做什么」。

本契约与具体 appCode 无关，所有应用目录下的 `feature/` 共享同一套职责定义。

## 应包含的内容

- 已确认存在的功能能力。
- 功能边界与范围。
- 主要业务流程与关键路径。

## 不应包含的内容

- 运行环境与基础配置事实：应放入 `base/`。
- 业务规则与研发规范：应放入 `rule/`。
- 技术约束与部署架构：应放入 `tech/`。
- 规划中、未确认的功能：先放入 `candidate/`，确认后再迁入本目录。

## 维护规则

- 只记录当前已确认存在的功能，不把规划能力当事实。
- 功能新增、变更后，必须回到当前应用代码核对，并同步更新 `verifiedAt`。
- 功能描述聚焦能力与流程边界，不复制实现细节。
