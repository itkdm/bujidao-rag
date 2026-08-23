---
id: KB-APP-{APP-CODE-UPPER}
type: application
scope: app
appCode: {appCode}
status: DRAFT
owner: {owner}
maintainers:
- {maintainer}
version: 1
updatedAt: {YYYY-MM-DD}
verifiedAt: {YYYY-MM-DD}
confidence: {high|medium|low}
stability: {stable|evolving|volatile}
evidence:
- type: code
  ref: {workspace-relative-build-or-entry-path}
tags:
- {tag}
anchors:
- APP:{APP-CODE-UPPER}
---

# {应用名称}

## AI 使用摘要

- 适用场景：{何时读取本总览}
- 关键入口：{构建、启动或运行入口}
- 关键规则：上游示例、目录或依赖存在不等于目标项目已采用对应能力
- 关联知识：[INDEX.md](./INDEX.md)
- 使用前必须核对：{易变事实}

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `{workspace-relative-path}` | {可验证事实} |

## 概述

说明当前应用是什么、不是什么，以及它在目标工作区中的职责。

## 基本信息

| 属性 | 当前值 |
| --- | --- |
| 应用编码 | `{appCode}` |
| 应用形态 | {单体、服务、前端、任务进程等} |
| 技术栈 | {从当前代码验证} |
| 构建入口 | `{path-or-command}` |
| 启动或部署入口 | `{path-or-command}` |

## 当前模块与能力边界

只记录当前代码和配置能够证明的模块、装配状态与边界。未确认内容进入 `candidate/`。

## 系统边界

说明该应用与其他应用、数据存储和外部系统的真实调用关系。

## 关键入口

| 对象 | 路径或名称 | 用途 |
| --- | --- | --- |
| {入口} | `{path}` | {用途} |

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| {问题} | 待确认 | {影响} |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | {YYYY-MM-DD} | 初始化应用总览 | {maintainer} |
