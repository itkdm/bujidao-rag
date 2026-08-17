---
# ==================== 必填字段 ====================
id: KB-APPLICATION-KUAYOU-001
type: application
scope: ruoyi-vue-pro
# 业务归属
domain: kuayou
application: ruoyi-vue-pro

# 应用类型：供 AI 工具自动识别，如 code-review 据此触发端面安全检查
appType: 后端应用

# 状态管理
status: DRAFT
authorship: human
owner: bujidao
maintainers:
  - bujidao
version: 3
updatedAt: 2026-08-09
verifiedAt: 2026-08-09
confidence: high
stability: evolving

# 证据
evidence:
  - type: code
    ref: ruoyi-vue-pro/
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/pom.xml
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java
    verifiedAt: 2026-08-09
  - type: doc
    ref: docs/06-tech/02-上游源码版本记录.md
  - type: human
    ref: 布吉岛确认当前尚未进行业务改造，2026-08-09

# 标签与锚点
tags:
  - backend
  - java17
  - spring-boot
  - ruoyi-vue-pro
  - yudao
anchors:
  - APPLICATION:ruoyi-vue-pro
  - CODEBASE:ruoyi-vue-pro
  - UPSTREAM:YunaiV/ruoyi-vue-pro
---

# ruoyi-vue-pro 后端开源基线

## AI 使用摘要

- 适用场景：需要了解夸友当前选定的 Java 后端开源底座、基线版本、模块现状和后续改造边界时
- 关键入口：`ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java`
- 关键规则：当前 `ruoyi-vue-pro/` 仍是上游开源项目本体，尚未完成夸友业务改造；不得把上游已有模块直接视为夸友已确认业务能力
- 关联知识：[INDEX.md](./INDEX.md)
- 使用前必须核对：根 `pom.xml` 启用模块、数据库脚本、配置文件、夸友业务改造 commit 是否有新增变化

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | 确认 Java 17、Spring Boot 版本、根工程当前启用模块 |
| code | `ruoyi-vue-pro/yudao-server/` | 确认后端启动模块与应用入口 |
| doc | `docs/06-tech/02-上游源码版本记录.md` | 记录上游仓库、基线分支与接入 commit |
| human | 布吉岛确认，2026-08-09 | 当前尚未对 `ruoyi-vue-pro` 进行夸友业务改造 |

## 概述

`ruoyi-vue-pro/` 是夸友主仓库中引入的 Java 后端开源基线，来源于上游 `YunaiV/ruoyi-vue-pro` 的 `master-jdk17` 分支。

在当前阶段，它不是已经完成定制的“夸友后端业务系统”，而是后续承载夸友后端能力的技术底座。本文档只记录当前开源基线的事实、可参考能力和改造边界。

---

## 基本信息

| 属性 | 值 |
| --- | --- |
| 应用编码 | `ruoyi-vue-pro` |
| 当前名称 | 后端开源基线 |
| 目标角色 | 夸友 Java 后端单体应用 |
| 来源仓库 | `https://github.com/YunaiV/ruoyi-vue-pro` |
| 基线分支 | `master-jdk17` |
| 接入 commit | `ec3f7cbf73e88514a70a6b59d365092ee470603d` |
| 定制状态 | 未改造 |
| 所属团队 | 夸友 |
| 负责人 | 布吉岛（bujidao） |
| 技术栈 | Java 17 / Spring Boot 3.5.15 / Maven |

---

## 当前事实

### 代码状态

当前目录保留了上游 `ruoyi-vue-pro` 的开源工程结构，已经移除子项目内部 `.git`，由夸友主仓库统一管理。

截至本文档更新时间，尚未记录任何夸友业务改造。因此，文档中涉及“夸友后端”的描述只能表达目标方向，不能表达已经上线或已经实现的业务事实。

### 根工程启用模块

根据 `ruoyi-vue-pro/pom.xml`，当前根 Maven 工程启用的模块为：

| 模块 | 当前状态 | 说明 |
| --- | --- | --- |
| `yudao-dependencies` | 已启用 | 依赖版本管理 |
| `yudao-framework` | 已启用 | 通用框架能力 |
| `yudao-server` | 已启用 | 后端启动入口 |
| `yudao-module-system` | 已启用 | 系统管理、用户、权限等基础能力 |
| `yudao-module-infra` | 已启用 | 基础设施能力 |

### 目录存在但未在根工程启用的模块

仓库中存在多个上游业务模块目录，但根 `pom.xml` 中对应 `<module>` 当前处于注释状态，不能直接视为夸友已启用能力。

| 模块 | 当前状态 | 后续判断 |
| --- | --- | --- |
| `yudao-module-member` | 未启用 | 学生/会员体系改造前需评估 |
| `yudao-module-mall` | 未启用 | 商城能力改造前需评估 |
| `yudao-module-pay` | 未启用 | 支付、结算能力改造前需评估 |
| `yudao-module-bpm` | 未启用 | 流程审批需求明确后再评估 |
| `yudao-module-report` | 未启用 | 报表需求明确后再评估 |
| `yudao-module-mp` | 未启用 | 公众号能力需求明确后再评估 |
| `yudao-module-crm` | 未启用 | 客户/商家运营需求明确后再评估 |
| `yudao-module-erp` | 未启用 | 进销存需求明确后再评估 |
| `yudao-module-iot` | 未启用 | 暂无明确需求 |
| `yudao-module-mes` | 未启用 | 暂无明确需求 |
| `yudao-module-wms` | 未启用 | 仓储需求明确后再评估 |
| `yudao-module-im` | 未启用 | 即时通讯需求明确后再评估 |
| `yudao-module-ai` | 未启用 | AI 能力需求明确后再评估 |

---

## 目标定位

### 后续可能承担的职责

`ruoyi-vue-pro` 后续可能被改造成夸友的后端单体，承担以下方向的能力：

- 平台用户、学生用户、运营人员、管理员等身份体系
- PC 管理后台所需的管理 API
- 学生端/小程序所需的业务 API
- 商品、订单、库存、帖子、审核、校园站点等夸友业务能力
- 权限、配置、字典、日志、文件、任务调度等基础平台能力

以上内容是目标定位，不代表当前代码已经完成夸友业务适配。

### 当前不应假设的内容

- 不应假设上游 `mall`、`member`、`pay` 等模块已经适配夸友业务
- 不应假设数据库表结构已经符合夸友产品规划
- 不应假设接口、权限、菜单、角色已经按夸友业务重新设计
- 不应假设 PC 管理后台和小程序端已经可以直接对接当前后端完成夸友闭环

---

## 系统边界

### 当前边界

```text
[上游 ruoyi-vue-pro 开源工程]
          |
          v
[夸友主仓库中的 ruoyi-vue-pro/ 后端基线]
          |
          v
[待进行夸友业务改造]
```

### 目标边界

```text
[yudao-ui-admin-vue3 管理后台] --+
                                +--> [ruoyi-vue-pro 夸友后端] --> [数据库/缓存/第三方服务]
[yudao-mall-uniapp 学生端] ------+
```

目标边界只用于后续架构规划。正式开发时，应以实际接口、配置、数据库和改造 commit 为准。

### 上游来源

| 系统 | 依赖内容 | 方式 |
| --- | --- | --- |
| `YunaiV/ruoyi-vue-pro` | Java 后端开源基线 | 源码接入 |

### 后续目标调用方

| 系统 | 目标依赖内容 | 调用方式 |
| --- | --- | --- |
| `yudao-ui-admin-vue3` | 管理后台 API | HTTP |
| `yudao-mall-uniapp` | 学生端/商城 API | HTTP |

---

## 核心模块

| 模块 | 当前事实 | 后续关注点 | 文档 |
| --- | --- | --- | --- |
| `yudao-server` | 后端启动模块，包含 `YudaoServerApplication` | 环境配置、模块装配、启动参数 | - |
| `yudao-framework` | 上游通用框架层 | 认证鉴权、异常、日志、事务、数据权限等约束 | - |
| `yudao-module-system` | 当前启用的系统模块 | 用户、角色、权限、菜单、租户等是否需要按夸友重构 | - |
| `yudao-module-infra` | 当前启用的基础设施模块 | 文件、配置、代码生成、定时任务等是否沿用 | - |
| `yudao-module-mall` | 目录存在但根工程未启用 | 若复用商城能力，需先评估模型、接口、订单链路与夸友产品是否匹配 | - |
| `yudao-module-member` | 目录存在但根工程未启用 | 若复用会员能力，需先评估学生用户体系和学校/校区维度 | - |
| `yudao-module-pay` | 目录存在但根工程未启用 | 若涉及支付结算，需先评估支付渠道、分账、退款和合规边界 | - |

---

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 是否直接启用 `mall/member/pay` 等上游模块 | 待确认 | 影响后端模块边界和数据库设计 |
| 夸友是否保留上游多租户、权限、菜单体系 | 待确认 | 影响管理后台和组织模型 |
| 学生、站长、楼栋主理人、商家等身份是否复用上游用户模型 | 待确认 | 影响账号体系和权限设计 |
| 当前 `yudao-ui/` 目录是否保留 | 待确认 | 夸友已有独立 `yudao-ui-admin-vue3/`，需避免前端入口混淆 |
| 数据库初始化脚本采用哪一套 | 待确认 | 影响本地启动、数据迁移和后续环境搭建 |

---

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 2 | 2026-08-09 | 改为后端开源基线定位，区分当前事实、目标定位与待确认边界 | 布吉岛 |
| 3 | 2026-08-09 | 按 application 模板原始规则校准知识 ID | 布吉岛 |