---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-APP-RUOYI-VUE-PRO-BASE-README
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
- GLOBAL:BASE-CONTRACT
---

# base/

## 目录定位

`base/` 是应用基础事实和代码定位层。用于帮助 Agent / 开发者快速定位当前项目真实存在的模块、接口、模型、数据和关键代码入口。

本契约与具体 appCode 无关，所有应用目录下的 `base/` 共享同一套职责定义。

## 应包含的内容

- 模块索引
- API / Controller 入口
- DTO / Model
- 数据库表
- 配置
- MQ / Job 入口
- 权限入口
- 关键代码路径
- 当前项目真实存在的基础事实
- 事实型索引

## 不应包含的内容

- 业务能力和业务流程：应放入 `feature/`。
- 必须满足的业务规则：应放入 `rule/`。
- 为什么这样实现、技术机制如何工作：应放入 `tech/`。
- base 不承担方案设计和机制解释。

## 维护规则

- 只记录可验证事实。
- 优先提供准确定位入口。
- 不把推测写成事实。
- 事实发生变化后应及时更新，并同步 `verifiedAt`。
- 不在 base 中展开大篇幅技术方案分析。
