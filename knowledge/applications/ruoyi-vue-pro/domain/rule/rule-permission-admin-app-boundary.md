---
# ==================== 必填字段 ====================
id: KB-RULE-KUAYOU-RUOYI-VUE-PRO-ADMIN-APP-PERMISSION
type: rule
scope: ruoyi-vue-pro
# 业务归属
domain: kuayou
application: ruoyi-vue-pro
appType: 后端应用

# 规则分类
ruleArea: permission
topic: admin-app-boundary

# 状态管理
status: DRAFT
authorship: human
owner: bujidao
maintainers:
  - bujidao
version: 1
updatedAt: 2026-08-09
verifiedAt: 2026-08-09
confidence: high
stability: evolving

# 证据
evidence:
  - type: code
    ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/dict/DictTypeController.java
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/app/
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-biz-data-permission/src/main/java/cn/iocoder/yudao/framework/datapermission/core/annotation/DataPermission.java
    verifiedAt: 2026-08-09
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/07.功能权限.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/08.数据权限.md

# 标签与锚点
tags:
  - backend
  - permission
  - admin
  - app
  - data-permission
anchors:
  - APPLICATION:ruoyi-vue-pro
  - RULE_AREA:permission
  - RULE_TOPIC:admin-app-boundary
---

# 后台与用户端权限边界规则

## AI 使用摘要

- 适用场景：新增 Controller、判断接口是否加 `@PreAuthorize`、判断是否能关闭数据权限、区分后台和用户端接口时
- 关键规则：admin/app 接口分开；管理后台接口通常需要功能权限；数据权限默认开启，关闭必须有明确理由
- 关联知识：[base-api-index.md](../base/base-api-index.md)、[base-permission-index.md](../base/base-permission-index.md)、[tech-security-permission.md](../../tech/tech-security-permission.md)
- 使用前必须核对：接口端类型、权限编码、数据权限影响范围、是否存在已确认业务例外

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `DictTypeController.java` | 管理后台接口使用 `@PreAuthorize` 示例 |
| code | `controller/app/` | app 端 Controller 单独放置 |
| code | `DataPermission.java` | 数据权限默认开启，可通过注解控制 |
| doc | `07.功能权限.md` | 官方说明管理后台接口通常使用 `@PreAuthorize` |
| doc | `08.数据权限.md` | 官方说明数据权限默认开启 |

## 规则范围

适用于 `ruoyi-vue-pro` 后端的管理后台接口、用户端接口、功能权限、数据权限和权限例外判断。

## 不适用范围

本文不定义夸友最终角色矩阵，不决定校园站长、楼栋主理人、学生等业务身份的完整权限。

## 规则正文

| 规则 | 内容 | 依据 |
| --- | --- | --- |
| 端侧隔离规则 | 管理后台接口放在 `controller.admin`，用户端/小程序接口放在 `controller.app`，两端接口和 VO 不应无条件混用 | 官方项目结构、`base-api-index.md` |
| 后台权限规则 | 管理后台敏感接口通常必须使用 `@PreAuthorize("@ss.hasPermission(...)")` 声明权限 | `DictTypeController.java`、官方功能权限文档 |
| app 权限规则 | 用户端接口不应直接套用后台菜单权限模型，除非有明确设计依据 | 官方功能权限文档 |
| 数据权限默认规则 | 数据权限默认开启，不加 `@DataPermission` 也会生效 | `DataPermission.java`、官方数据权限文档 |
| 数据权限例外规则 | 使用 `@DataPermission(enable = false)` 必须有明确原因，例如查询自身必要信息或系统公共信息 | 现有代码注释、官方数据权限文档 |
| 权限编码规则 | 权限编码必须和菜单/按钮权限保持一致，不能只在 Controller 中孤立新增 | `base-permission-index.md` |

## 例外情况

- 无需登录或公共下拉数据接口，可以不加后台权限，但必须能解释使用场景。
- 系统自身信息、公共配置、避免查询自身数据被过滤等场景，可以关闭数据权限，但必须有注释或文档依据。
- 后续夸友若设计独立学生端权限体系，应新增规则文档，不能沿用本规则推断。

## 违反规则的风险

- 后台接口无权限保护，可能导致越权操作。
- app 接口误套后台菜单权限，可能导致学生端不可用或权限模型混乱。
- 随意关闭数据权限，可能导致跨组织、跨学校、跨角色数据泄露。
- 权限编码和菜单不一致，会导致接口 403 或按钮权限失效。

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `domain/base/` | API 和权限入口见 `base-api-index.md`、`base-permission-index.md` |
| `tech/` | 权限实现约束见 `tech-security-permission.md` |
| `domain/feature/` | 具体功能流程后续引用对应权限规则 |

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友是否沿用上游 RBAC | 待确认 | 影响后台菜单和权限编码 |
| 学生端是否建立独立权限体系 | 待确认 | 影响 app 接口鉴权方式 |
| 校园站长/楼栋主理人数据范围如何实现 | 待确认 | 影响数据权限规则 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |