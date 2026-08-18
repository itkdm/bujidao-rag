---
# 应用四类固定目录契约标准源：Rule
# 本文件是 application 下 rule/ 目录 README 的唯一正文标准源。
# 所有 knowledge/applications/{appCode}/rule/README.md 的正文必须与此完全一致。
# 本文件不绑定任何 appCode，不允许 application 自行改写目录职责。
id: KB-INFRA-TEMPLATE-APP-RULE-README
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- infrastructure
- template
- contract
- rule
anchors:
- GLOBAL:RULE-CONTRACT
---

# Rule

## 目录定位

`rule/` 用于记录当前应用必须成立的业务规则、系统规则和行为边界。

Rule 主要回答：

> 做这件事必须满足什么？

核心语义是：

> What must be true.

这里关注的是必须遵守的约束和边界，而不是具体采用什么代码或技术方式实现这些约束。

## 应包含的内容

本目录适合记录：

- 业务规则
- 权限规则
- 状态约束
- 数据边界
- 安全边界
- 业务一致性约束
- 功能之间必须满足的约束关系
- 应用级必须成立的系统行为
- 禁止行为和必要前置条件
- 对业务结果具有约束作用的长期规则

Rule 应能够帮助开发者和 Coding Agent 判断：

> 某个实现或行为是否允许，以及最终必须满足哪些条件。

## 不应包含的内容

以下内容不属于 Rule：

- 功能能力和主要业务流程，应进入 `feature/`
- API、Model、数据库表、代码路径等事实定位，应进入 `base/`
- 具体框架使用方式、事务、缓存、MQ、安全技术实现等内容，应进入 `tech/`
- Git Commit、Git Branch、Pull Request、通用编码规范等跨应用研发规范，应进入 `main/` 下对应的全局知识目录

不要因为某个内容名称中包含“规范”或“规则”，就默认应该进入 application `rule/`。

Rule 不负责详细解释技术上如何实现。

## 维护规则

- Rule 重点表达必须成立的条件、约束和边界
- 优先记录具有长期稳定价值的规则，不记录一次任务中的临时要求
- 不把具体技术实现方式写成规则本身
- 不把跨应用的通用研发规范复制到 application Rule
- 当业务规则、权限边界、状态约束或其他系统规则发生变化时，应同步更新
- 避免与 Feature、Base、Tech 重复记录相同层面的内容
