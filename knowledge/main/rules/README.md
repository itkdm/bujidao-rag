---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-MAIN-RULES-README
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
- GLOBAL:MAIN-RULES-README
---

# rules/

## 目录定位

`main/rules/` 存放**跨应用、跨系统、跨业务线**统一遵守的协作规范与业务规则，是团队共用的「应该怎么协作」约束来源。

## 应包含的内容

- 跨应用统一的研发协作规范（编码、分支、提交、评审、Agent 行为等）。
- 多应用都要遵守的全局业务规则与边界约束。

## 不应包含的内容

- 仅影响单个应用的应用内规则：应放入对应 `applications/{appCode}/rule/`。
- 基础事实与配置：应放入对应应用的 `base/`。
- 功能能力与业务流程：应放入对应应用的 `feature/`。
- 应用级技术约束与部署架构：应放入对应应用的 `tech/`。

## 维护规则

- 只有「跨应用强制统一」的规范才放入本目录，单一应用相关的规则不放入。
- 规则变更需经确认后更新，并同步 `verifiedAt`。
- 规则描述聚焦约束本身，不复制实现代码。
