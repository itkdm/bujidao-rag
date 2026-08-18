---
id: KB-INFRA-RUOYI-BASE-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- infrastructure
- readme
anchors:
- GLOBAL:RUOYI-BASE-README
---

# base/

## 本目录负责什么

`base/` 回答：**当前真实事实和代码入口在哪里？**

沉淀可验证的事实定位，是事实定位层。

## 什么内容应该放这里

- 模块
- API
- DTO / Model
- Repository
- 数据库表
- 配置
- MQ
- 权限入口
- 关键代码路径
- 其他可验证事实定位

## 什么内容不应该放这里，以及应该去哪里

- 为什么这样设计、业务流程解释 → `feature/`
- 技术方案展开 → `tech/`
- 业务规则定义 → `rule/`
- 主观推断或未经确认的事实 → 回到代码与证据确认，不要写成事实

## 新增本类知识时需要遵守的最基本归属原则

只记录可验证的事实与代码入口；不做设计解释，不展开技术方案，不定义业务规则。
