---
id: KB-BASE-RUOYI-VUE-PRO-MODEL
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
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/dataobject/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/api/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/enums/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md
tags:
- backend
- model
- vo
- dto
- do
anchors:
- APP:RUOYI-VUE-PRO
- BASE:MODEL
---

# 模型对象索引

## AI 使用摘要

- 适用场景：查找 DO、ReqVO、RespVO、DTO、Enum、ErrorCode 的位置和命名时
- 关键入口：`controller/**/vo`、`dal/dataobject`、`api/**/dto`、`enums`
- 关键事实：Controller 不直接暴露 DO；DO 在 `dal.dataobject`；错误码集中在模块 `enums/ErrorCodeConstants.java`
- 关联知识：[tech-framework-web-api.md](../../tech/tech-framework-web-api.md)、[tech-data-mybatis-cache.md](../../tech/tech-data-mybatis-cache.md)
- 使用前必须核对：模型属于接口层、数据层、跨模块 API，还是枚举/错误码

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `controller/admin/**/vo/` | ReqVO、RespVO 示例 |
| code | `dal/dataobject/` | DO 示例 |
| code | `api/**/dto/` | 模块间 DTO 示例 |
| code | `enums/` | 枚举和错误码入口 |
| doc | `09.项目结构.md` | 官方模型分层说明 |

## 索引范围

本文索引后端常见模型对象类型、命名后缀、放置路径和代表示例。

## 不收录范围

本文不描述字段含义和表结构细节；具体字段语义应进入更细的 `base-database-*` 或业务知识。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| ReqVO | `controller/{admin|app}/**/vo/**/*ReqVO.java` | 接口入参 | Controller 请求对象 |
| RespVO | `controller/{admin|app}/**/vo/**/*RespVO.java` | 接口出参 | Controller 响应对象 |
| PageReqVO | `*PageReqVO.java` | 分页入参 | 通常继承 `PageParam` |
| SimpleRespVO | `*SimpleRespVO.java` | 轻量出参 | 下拉框、简单列表 |
| DO | `dal/dataobject/**/*DO.java` | 数据对象 | 数据库表映射对象 |
| DTO | `api/**/dto/**/*DTO.java` | 跨模块传输对象 | 模块间 API 入参/出参 |
| Enum | `enums/**/*Enum.java` | 枚举 | 状态、类型、场景等 |
| ErrorCode | `enums/ErrorCodeConstants.java` | 错误码 | 模块错误码集中定义 |

## 命名与定位规则

- 数据库实体以 `DO` 结尾，放在 `dal.dataobject`。
- Controller 入参以 `ReqVO` 结尾，出参以 `RespVO` 结尾。
- 跨模块 API 对象以 `DTO` 结尾，放在 `api/**/dto`。
- 枚举通常以 `Enum` 结尾，放在 `enums` 或其子包。
- 错误码统一放在模块 `enums/ErrorCodeConstants.java`。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `yudao-module-system/.../controller/admin/**/vo/` | 管理后台 VO | 当前主要接口模型入口 |
| `yudao-module-system/.../controller/app/**/vo/` | app 端 VO | 当前 app 接口模型入口 |
| `yudao-module-system/.../dal/dataobject/` | DO | 数据库映射对象 |
| `yudao-module-system/.../api/**/dto/` | DTO | 模块间调用模型 |
| `yudao-module-system/.../enums/` | 枚举/错误码 | 模块常量入口 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | VO/DO/DTO 使用约束见 Web API 和 MyBatis tech 文档 |
| `domain/feature/` | 功能流程会引用对应 ReqVO/RespVO |
| `domain/rule/` | 状态枚举和错误码通常反映业务规则 |

## 变更影响

模型对象改名、移动或字段调整会影响 Controller、前端调用、数据库映射、跨模块 API、接口文档和测试。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友业务模块是否使用独立模型包 | 待确认 | 影响模型索引扩展 |
| app 端和 admin 端 VO 是否严格隔离 | 待确认 | 影响接口安全边界 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |