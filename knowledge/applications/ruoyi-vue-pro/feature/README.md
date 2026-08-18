---
# 知识库导航基础设施文件
id: KB-INFRA-APP-RUOYI-VUE-PRO-FEATURE-README
scope: app
appCode: ruoyi-vue-pro
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 2
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- application
anchors:
- APP:RUOYI-VUE-PRO
- FEATURE:RUOYI-VUE-PRO
---

# feature/

## 目录定位

`feature/` 记录 RuoYi-Vue-Pro 应用**当前已确认的功能能力**与主要业务流程，描述系统「能做什么」。

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
