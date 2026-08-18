---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-YUDAO-BASE-README
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

`base/` 是应用知识目录下存放**稳定、可定位的基础事实**的目录，是其他知识的共同事实底座。例如运行环境、依赖库版本、部署方式、基础配置项等不易变化、可作为定位入口的信息。

本契约与具体 appCode 无关，所有应用目录下的 `base/` 共享同一套职责定义。

## 应包含的内容

- 应用运行环境、依赖库与框架版本。
- 部署方式与基础配置项（如端口、数据源、中间件连接）。
- 稳定、可定位、可作为其他知识引用锚点的基础事实。

## 不应包含的内容

- 功能能力与业务流程：应放入 `feature/`。
- 业务规则与研发规范：应放入 `rule/`。
- 易变的技术约束与架构细节：应放入 `tech/`。
- 动态内容摘要、当前文件清单：应放入本目录 `INDEX.md`。

## 维护规则

- 只记录当前已确认、稳定存在的基础事实，不把规划或推断当作事实。
- 基础事实变化（如版本升级、配置调整）后，必须回到真实代码 / 配置核对并更新，同时更新 `verifiedAt`。
- 只提供定位入口，不复制大段易变配置细节。
