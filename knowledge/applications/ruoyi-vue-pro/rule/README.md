---
# 知识库导航基础设施文件
id: KB-INFRA-APP-RUOYI-VUE-PRO-RULE-README
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
- RULE:RUOYI-VUE-PRO
---

# rule/

## 目录定位

`rule/` 存放 RuoYi-Vue-Pro 应用范围内的**业务规则与研发规范**，约束「应该怎么做」。

## 应包含的内容

- 该应用范围内的业务规则与约束。
- 研发规范（编码规范、代码提交规范、分支与评审规范等）。
- 团队在该应用中约定遵守的强制性规则。

## 不应包含的内容

- 基础事实与配置：应放入 `base/`。
- 功能能力与业务流程：应放入 `feature/`。
- 技术约束与部署架构细节：应放入 `tech/`。
- 跨应用统一的全局规则：应放入 `main/rules/`。

## 维护规则

- 只记录当前已确认、团队约定遵守的规则，不把临时约定当正式规则。
- 规则变更需经确认后更新，并同步 `verifiedAt`。
- 规则描述聚焦约束本身，不复制实现代码。
