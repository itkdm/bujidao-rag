---
# 知识库导航基础设施文件（全局目录契约，与具体应用无关）
id: KB-INFRA-YUDAO-TECH-README
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
- GLOBAL:TECH-CONTRACT
---

# tech/

## 目录定位

`tech/` 用于记录应用技术实现方式、工程实践、技术机制和实现约束。核心问题：「在当前应用和技术栈中应该怎么实现？」核心语义：`tech = How we implement it`。

本契约与具体 appCode 无关，所有应用目录下的 `tech/` 共享同一套职责定义。

## 应包含的内容

- 系统架构
- 模块边界
- Web / API 实现
- Controller / Service 等工程约定
- 数据访问、MyBatis
- 事务
- 缓存
- MQ、异步任务
- 权限技术实现
- 异常处理、日志
- 构建环境、测试
- 框架使用方式
- 技术选型在当前应用中的具体落地

tech 承担的是完整的应用技术实现知识，不应被缩窄成「部署架构」或「纯技术约束」。

## 不应包含的内容

- 业务功能流程：应放入 `feature/`。
- 必须成立的业务规则：应放入 `rule/`。
- 单纯代码 / API / 表事实定位：应放入 `base/`。
- 跨应用 Git 等通用研发规范：应由 `main/` 下对应全局知识承担。

## 维护规则

- 重点解释当前项目技术上怎么实现。
- 必须以当前实际代码和技术栈为依据。
- 不把纯业务规则混入 tech。
