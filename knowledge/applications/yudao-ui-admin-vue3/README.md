---
# 知识库导航基础设施文件
id: KB-INFRA-APP-YUDAO-UI-ADMIN-VUE3-README
scope: app
appCode: yudao-ui-admin-vue3
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- application
anchors:
- APP:YUDAO-UI-ADMIN-VUE3
- GLOBAL:APPLICATION-README
---

# yudao-ui-admin-vue3/

## 目录定位

`applications/yudao-ui-admin-vue3/` 是芋道 yudao-ui-admin-vue3 应用的「应用层」知识目录，集中存放该应用范围内的知识，与 `main/` 的跨应用通用知识相互区分。

## 应包含的内容

- 应用总览：根目录的 `yudao-ui-admin-vue3.md`，描述该应用本身是什么。
- 基础事实：`base/` 存放该应用稳定、可定位的基础事实与配置索引。
- 功能能力：`feature/` 存放已确认的功能能力与主要业务流程。
- 业务规则：`rule/` 存放该应用范围内的业务规则与编码规范。
- 技术约束：`tech/` 存放该应用级的技术约束与部署架构。

## 不应包含的内容

- 跨应用统一、需要全员遵守的通用知识：应放入 `main/`。
- 未确认推断：应放入 `candidate/`。
- 个人经验与碎片素材：应放入 `personal/`。
- 应用的实际业务信息（技术栈、核心模块、业务目标、系统边界等）：属于 `yudao-ui-admin-vue3.md`，不写进本目录 README。

## 维护规则

- 本目录只描述「应用知识如何组织与维护」，不承载应用实际业务信息。
- 新增、修改、删除本目录内容时，遵守各子目录 README 的局部维护规则。
- 所有知识文件必须遵守 `KNOWLEDGE-METADATA-RULES.md`，并通过 `scripts/validate_metadata.py` 校验。
