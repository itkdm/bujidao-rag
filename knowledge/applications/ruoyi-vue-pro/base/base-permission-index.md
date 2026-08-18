---
id: KB-BASE-RUOYI-VUE-PRO-PERMISSION
type: base
scope: app
appCode: ruoyi-vue-pro
status: DRAFT
owner: bujidao
maintainers:
- bujidao
version: 2
updatedAt: 2026-08-18
verifiedAt: 2026-08-09
confidence: high
stability: evolving
evidence:
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/permission/
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-security/src/main/java/cn/iocoder/yudao/framework/security/core/service/SecurityFrameworkServiceImpl.java
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-biz-data-permission/src/main/java/cn/iocoder/yudao/framework/datapermission/core/annotation/DataPermission.java
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/07.功能权限.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/08.数据权限.md
tags:
- backend
- permission
- rbac
- data-permission
anchors:
- APP:RUOYI-VUE-PRO
- BASE:PERMISSION
---

# 权限事实索引

## AI 使用摘要

- 适用场景：定位权限 Controller、权限 API、`@PreAuthorize`、`@DataPermission`、角色/菜单/部门相关入口时
- 关键入口：`controller/admin/permission/`、`SecurityFrameworkServiceImpl`、`DataPermission`
- 关键事实：管理后台接口通过 `@PreAuthorize` 绑定权限编码；数据权限默认开启；权限相关业务入口集中在 system 模块
- 关联知识：[tech-security-permission.md](../../tech/tech-security-permission.md)
- 使用前必须核对：目标接口是否 admin 端、权限编码是否存在、数据权限是否影响查询

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `controller/admin/permission/` | 菜单、角色、权限分配接口入口 |
| code | `SecurityFrameworkServiceImpl.java` | `@ss` 权限判断实现 |
| code | `DataPermission.java` | 数据权限注解 |
| doc | `07.功能权限.md` | 官方功能权限说明 |
| doc | `08.数据权限.md` | 官方数据权限说明 |

## 索引范围

本文索引权限相关 Controller、API、注解、枚举和数据权限入口。

## 不收录范围

本文不定义夸友业务角色和权限矩阵；角色规则应进入 `rule/` 或正式产品文档。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| 菜单 Controller | `controller/admin/permission/MenuController.java` | Controller | 菜单管理入口 |
| 角色 Controller | `controller/admin/permission/RoleController.java` | Controller | 角色管理入口 |
| 权限分配 Controller | `controller/admin/permission/PermissionController.java` | Controller | 角色菜单、数据权限、用户角色分配 |
| 权限 API | `api/permission/PermissionApi.java` | Java interface | 跨模块权限能力 |
| 权限 API 实现 | `api/permission/PermissionApiImpl.java` | Java class | 权限 API 实现 |
| 权限服务实现 | `SecurityFrameworkServiceImpl` | Java class | `@ss.hasPermission/hasRole/hasScope` 实现 |
| 数据权限注解 | `DataPermission.java` | Java annotation | 控制数据权限开关和规则 |
| 数据范围枚举 | `enums/permission/DataScopeEnum.java` | Enum | 数据权限范围枚举 |

## 命名与定位规则

- 管理后台功能权限常见格式：`{module}:{resource}:{action}`。
- 权限判断常见注解：`@PreAuthorize("@ss.hasPermission('...')")`。
- 数据权限注解：`@DataPermission`，默认开启。
- 角色、菜单、权限相关代码集中在 `system` 模块的 `permission` 包。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `yudao-module-system/.../controller/admin/permission/` | 权限管理 API | 菜单、角色、权限分配 |
| `yudao-module-system/.../service/permission/` | 权限业务逻辑 | 角色、菜单、权限关系 |
| `yudao-framework/.../security/core/service/SecurityFrameworkServiceImpl.java` | 权限表达式实现 | `@ss` Bean 实现入口 |
| `yudao-framework/.../datapermission/core/annotation/DataPermission.java` | 数据权限注解 | 默认启用，可禁用 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | 权限使用约束见 `tech-security-permission.md` |
| `feature/` | 功能流程会引用具体接口权限 |
| `rule/` | 角色权限矩阵应进入 rule |

## 变更影响

权限入口变化会影响后台菜单、按钮权限、接口访问控制、数据范围过滤和前端权限展示。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友是否沿用上游 RBAC | 待确认 | 影响权限表和接口注解 |
| 校园站长/楼栋主理人如何映射数据权限 | 待确认 | 影响数据范围规则 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |