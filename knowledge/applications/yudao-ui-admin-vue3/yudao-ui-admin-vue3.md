---
# ==================== 必填字段 ====================
id: KB-APPLICATION-KUAYOU-002
type: application
scope: yudao-ui-admin-vue3
# 业务归属
domain: kuayou
application: yudao-ui-admin-vue3

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
    ref: yudao-ui-admin-vue3/
    verifiedAt: 2026-08-09
  - type: code
    ref: yudao-ui-admin-vue3/package.json
    verifiedAt: 2026-08-09
  - type: doc
    ref: docs/06-tech/01-技术底座与仓库结构.md
  - type: doc
    ref: docs/06-tech/02-上游源码版本记录.md
  - type: human
    ref: 布吉岛确认当前尚未进行业务改造，2026-08-09

# 标签与锚点
tags:
  - admin
  - vue3
  - element-plus
  - pc
anchors:
  - APPLICATION:yudao-ui-admin-vue3
  - BIZ_IDENTITY:平台运营
  - BIZ_IDENTITY:系统管理员
---

# yudao-ui-admin-vue3

## AI 使用摘要

- 适用场景：需要了解夸友当前选定的 PC 管理后台前端基线、来源版本、技术栈和后续改造边界时
- 关键入口：`yudao-ui-admin-vue3/package.json`
- 关键规则：当前 `yudao-ui-admin-vue3/` 仍是上游开源项目本体，尚未完成夸友业务改造；不得把上游页面和菜单直接视为夸友已确认后台能力
- 关联知识：[INDEX.md](./INDEX.md)
- 使用前必须核对：路由、API 封装、权限菜单、环境配置、夸友业务改造 commit 是否有新增变化

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `yudao-ui-admin-vue3/package.json` | 确认项目名称、版本、Vue3、Element Plus、Vite 等依赖 |
| doc | `docs/06-tech/02-上游源码版本记录.md` | 记录上游基线分支与接入 commit |
| human | 布吉岛确认，2026-08-09 | 当前尚未对 `yudao-ui-admin-vue3` 进行夸友业务改造 |

## 概述

`yudao-ui-admin-vue3/` 是夸友主仓库中引入的 PC 管理后台前端基线，来源于上游 `yudaocode/yudao-ui-admin-vue3` 的 `master` 分支。

在当前阶段，它不是已经完成定制的“夸友 PC 管理后台”，而是后续改造后台运营界面的前端底座。本文档只记录当前开源基线的事实、可参考能力和改造边界。

---

## 基本信息

| 属性 | 值 |
| --- | --- |
| 应用编码 | `yudao-ui-admin-vue3` |
| 当前名称 | PC 管理后台开源基线 |
| 目标角色 | 夸友 PC 管理后台 |
| 来源仓库 | `https://github.com/yudaocode/yudao-ui-admin-vue3` |
| 基线分支 | `master` |
| 接入 commit | `d4b521a169ff430824ec92235dc4a0fec378f253` |
| 定制状态 | 未改造 |
| 所属团队 | 夸友 |
| 负责人 | 布吉岛（bujidao） |
| 技术栈 | Vue3 / Element Plus / Vite / TypeScript / pnpm |

---

## 系统职责

### 当前事实

当前目录保留了上游 PC 管理后台的开源工程结构，尚未记录夸友业务改造。上游已有页面、菜单、权限、接口封装只能作为改造参考，不能直接视为夸友后台的最终功能范围。

### 目标职责

后续可能改造为夸友平台运营和管理员使用的后台管理界面，调用后端 API 完成业务配置、审核、查询和管理。

### 当前不应假设的内容

- 不应假设商品、订单、库存、帖子审核、用户管理等页面已经符合夸友产品规划
- 不应假设权限菜单、路由和接口路径已经完成夸友业务适配
- 不应假设当前后台已经可以直接对接后端完成夸友业务闭环
- 不负责后端业务规则实现，不负责学生端小程序交互，不直接持久化业务数据

---

## 系统边界

### 当前边界

```text
[上游 yudao-ui-admin-vue3 开源工程]
            |
            v
[夸友主仓库中的 yudao-ui-admin-vue3/ 前端基线]
            |
            v
[待进行夸友业务改造]
```

### 目标边界

```text
[平台运营/管理员] --> [yudao-ui-admin-vue3 夸友管理后台] --> [ruoyi-vue-pro 夸友后端]
```

### 上游来源

| 系统 | 依赖内容 | 方式 |
| --- | --- | --- |
| `yudaocode/yudao-ui-admin-vue3` | PC 管理后台前端基线 | 源码接入 |

### 后续目标依赖

| 系统 | 目标依赖内容 | 调用方式 |
| --- | --- | --- |
| `ruoyi-vue-pro` | 管理后台 API | HTTP |

---

## 核心模块

| 模块 | 职责 | 核心类 | 文档 |
| --- | --- | --- | --- |
| `src/` | 上游管理后台源码 | 待补充 | - |
| `src/api/` | 上游 API 请求封装 | 待补充 | - |
| `src/views/` | 上游页面视图 | 待补充 | - |
| `package.json` | 项目配置与依赖 | - | - |

---

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 2 | 2026-08-09 | 改为 PC 管理后台开源基线定位，并按 application 模板原始规则校准知识 ID | 布吉岛 |