---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-YUDAO-RULE-README
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
- GLOBAL:RULE-CONTRACT
---

# rule/

## 目录定位

`rule/` 用于记录当前应用必须成立的业务规则、系统规则和行为边界。核心问题：「做这件事必须满足什么规则和边界？」核心语义：`rule = What must be true`。

本契约与具体 appCode 无关，所有应用目录下的 `rule/` 共享同一套职责定义。

## 应包含的内容

- 业务规则
- 权限规则
- 状态约束
- 数据边界
- 安全边界
- 业务一致性约束
- 应用级必须遵守的行为规则
- 功能之间必须满足的约束关系

## 不应包含的内容

- Git Commit 规范、Git Branch 规范、Pull Request 规范、通用编码风格、通用开发流程规范等跨应用研发规范：应由 `main/` 下的全局知识承担。
- 具体技术实现方式：应放入 `tech/`。
- 代码 / API / 表的位置：应放入 `base/`。
- 功能流程本身：应放入 `feature/`。

## 维护规则

- rule 重点表达「什么必须成立」。
- 不展开「具体怎么实现」。
- 不重复 tech 中的工程实现细节。
- 不把所有带有「规范」二字的内容都归到 rule。
