---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-APPLICATIONS-README
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- global
anchors:
- GLOBAL:APPLICATIONS-README
---

# applications/

## 目录定位

`knowledge/applications/` 按应用或模块组织知识，是「应用层」知识的统一容器。每个子目录对应一个已注册的应用（appCode），承载该应用范围内的知识。

## 应包含的内容

- 每个已注册应用一个独立子目录：`applications/{appCode}/`。
- 应用级知识按四类子目录组织：`base/`（基础事实）、`feature/`（功能能力）、`rule/`（业务规则）、`tech/`（技术约束）。
- 每个应用根目录下的 `{appCode}.md`：描述该应用本身是什么。

## 不应包含的内容

- 跨应用统一、需要全员遵守的通用知识：应放入 `main/`。
- 未确认推断：应放入 `candidate/`。
- 个人经验与碎片素材：应放入 `personal/`。
- 应用实际业务信息（技术栈、核心模块、业务目标等）：属于各应用的 `{appCode}.md`，不写进本目录 README。

## 维护规则

- 新增应用前必须先按 `KNOWLEDGE-METADATA-RULES.md` 的 AppCode Registry 注册 appCode。
- 每个应用目录统一包含 `README.md`、`INDEX.md`、`{appCode}.md` 及四类子目录（base / feature / rule / tech）。
- 应用层知识的新增、修改、删除遵循对应子目录 README 的局部维护规则。
