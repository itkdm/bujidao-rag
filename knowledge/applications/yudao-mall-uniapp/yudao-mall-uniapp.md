---
# ==================== 必填字段 ====================
id: KB-APPLICATION-KUAYOU-003
type: application
scope: yudao-mall-uniapp
# 业务归属
domain: kuayou
application: yudao-mall-uniapp

# 应用类型：供 AI 工具自动识别，如 code-review 据此触发端面安全检查
appType: 前端应用

# 状态管理
status: DRAFT
authorship: human
owner: bujidao
maintainers:
  - bujidao
version: 2
updatedAt: 2026-08-09
verifiedAt: 2026-08-09
confidence: high
stability: evolving

# 证据
evidence:
  - type: code
    ref: yudao-mall-uniapp/
    verifiedAt: 2026-08-09
  - type: code
    ref: yudao-mall-uniapp/package.json
    verifiedAt: 2026-08-09
  - type: doc
    ref: docs/06-tech/01-技术底座与仓库结构.md
  - type: doc
    ref: docs/06-tech/02-上游源码版本记录.md
  - type: human
    ref: 布吉岛确认当前尚未进行业务改造，2026-08-09

# 标签与锚点
tags:
  - mini-program
  - uniapp
  - mall
  - vue3
anchors:
  - APPLICATION:yudao-mall-uniapp
  - BIZ_IDENTITY:学生用户
---

# yudao-mall-uniapp

## AI 使用摘要

- 适用场景：需要了解夸友当前选定的学生端/商城小程序前端基线、来源版本、技术栈和后续改造边界时
- 关键入口：`yudao-mall-uniapp/package.json`
- 关键规则：当前 `yudao-mall-uniapp/` 仍是上游开源项目本体，尚未完成夸友业务改造；不得把上游商城页面和流程直接视为夸友已确认学生端能力
- 关联知识：[INDEX.md](./INDEX.md)
- 使用前必须核对：页面路径、接口配置、平台兼容、微信小程序构建方式、夸友业务改造 commit 是否有新增变化

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `yudao-mall-uniapp/package.json` | 确认项目名称、展示名称、版本、uni-app 与 Vue3 能力 |
| doc | `docs/06-tech/02-上游源码版本记录.md` | 记录上游基线分支与接入 commit |
| human | 布吉岛确认，2026-08-09 | 当前尚未对 `yudao-mall-uniapp` 进行夸友业务改造 |

## 概述

`yudao-mall-uniapp/` 是夸友主仓库中引入的学生端/商城小程序前端基线，来源于上游 `yudaocode/yudao-mall-uniapp` 的 `master` 分支。

在当前阶段，它不是已经完成定制的“夸友学生端小程序”，而是后续改造学生端体验的前端底座。本文档只记录当前开源基线的事实、可参考能力和改造边界。

---

## 基本信息

| 属性 | 值 |
| --- | --- |
| 应用编码 | `yudao-mall-uniapp` |
| 当前名称 | 学生端/商城小程序开源基线 |
| 目标角色 | 夸友学生端小程序 |
| 来源仓库 | `https://github.com/yudaocode/yudao-mall-uniapp` |
| 基线分支 | `master` |
| 接入 commit | `88b5be678d08ce9a729d8395f8c25f80a274a54c` |
| 定制状态 | 未改造 |
| 所属团队 | 夸友 |
| 负责人 | 布吉岛（bujidao） |
| 技术栈 | uni-app / Vue3 / Pinia |

---

## 系统职责

### 当前事实

当前目录保留了上游商城 uni-app 的开源工程结构，尚未记录夸友业务改造。上游已有页面、接口、商城流程只能作为改造参考，不能直接视为夸友学生端的最终功能范围。

### 目标职责

后续可能改造为学生用户使用的移动端/微信小程序体验，承载商城浏览、商品下单、个人中心，以及校园互动、活动和楼栋场景等能力。

### 当前不应假设的内容

- 不应假设上游商城页面已经符合夸友学生端产品规划
- 不应假设商品、订单、会员、支付等流程已经完成夸友业务适配
- 不应假设当前小程序已经可以直接对接后端完成夸友业务闭环
- 不负责后端业务规则实现，不负责 PC 管理后台运营功能，不直接维护全局业务规则

---

## 系统边界

### 当前边界

```text
[上游 yudao-mall-uniapp 开源工程]
            |
            v
[夸友主仓库中的 yudao-mall-uniapp/ 前端基线]
            |
            v
[待进行夸友业务改造]
```

### 目标边界

```text
[学生用户] --> [yudao-mall-uniapp 夸友学生端] --> [ruoyi-vue-pro 夸友后端]
```

### 上游来源

| 系统 | 依赖内容 | 方式 |
| --- | --- | --- |
| `yudaocode/yudao-mall-uniapp` | 学生端/商城小程序前端基线 | 源码接入 |

### 后续目标依赖

| 系统 | 目标依赖内容 | 调用方式 |
| --- | --- | --- |
| `ruoyi-vue-pro` | 学生端/商城 API | HTTP |

---

## 核心模块

| 模块 | 职责 | 核心类 | 文档 |
| --- | --- | --- | --- |
| `pages/` | 上游小程序页面 | 待补充 | - |
| `sheep/` | 上游商城模板核心能力 | 待补充 | - |
| `package.json` | 项目配置与依赖 | - | - |

---

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 2 | 2026-08-09 | 改为学生端/商城小程序开源基线定位，并按 application 模板原始规则校准知识 ID | 布吉岛 |