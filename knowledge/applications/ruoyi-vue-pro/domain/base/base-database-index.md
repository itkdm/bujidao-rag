---
id: KB-BASE-RUOYI-VUE-PRO-DATABASE
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
  ref: ruoyi-vue-pro/sql/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/dataobject/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/mysql/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/25.MyBatis 数据库.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/44.数据库文档.md
tags:
- backend
- database
- sql
- mybatis
anchors:
- APP:RUOYI-VUE-PRO
- BASE:DATABASE
---

# 数据库与 SQL 索引

## AI 使用摘要

- 适用场景：定位 SQL 脚本、数据库表映射、Mapper、Quartz 表、数据库文档入口时
- 关键入口：`ruoyi-vue-pro/sql/`、`dal/dataobject`、`dal/mysql`
- 关键事实：多数据库 SQL 分目录存放；MySQL 主脚本为 `sql/mysql/ruoyi-vue-pro.sql`；Quartz 表脚本为各数据库目录下 `quartz.sql`
- 关联知识：[tech-data-mybatis-cache.md](../../tech/tech-data-mybatis-cache.md)
- 使用前必须核对：目标数据库类型、模块是否启用、SQL 是否与当前代码版本一致

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/sql/` | 多数据库 SQL 脚本目录 |
| code | `dal/dataobject/` | 表映射 DO |
| code | `dal/mysql/` | Mapper 入口 |
| doc | `25.MyBatis 数据库.md` | 官方 MyBatis 与数据库规范 |
| doc | `44.数据库文档.md` | 官方数据库文档入口说明 |

## 索引范围

本文索引 SQL 脚本位置、数据库类型目录、DO/Mapper 路径和基础表结构定位方式。

## 不收录范围

本文不记录完整建表 SQL 和字段解释；字段级语义应按业务模块继续拆分。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| SQL 根目录 | `ruoyi-vue-pro/sql/` | directory | 多数据库脚本入口 |
| MySQL 主脚本 | `sql/mysql/ruoyi-vue-pro.sql` | SQL | MySQL 初始化主脚本 |
| MySQL Quartz 脚本 | `sql/mysql/quartz.sql` | SQL | Quartz 表初始化脚本 |
| PostgreSQL 脚本 | `sql/postgresql/` | directory | PostgreSQL 初始化脚本 |
| Oracle 脚本 | `sql/oracle/` | directory | Oracle 初始化脚本 |
| SQL Server 脚本 | `sql/sqlserver/` | directory | SQL Server 初始化脚本 |
| DO 路径 | `yudao-module-system/.../dal/dataobject/` | Java package | 表映射对象 |
| Mapper 路径 | `yudao-module-system/.../dal/mysql/` | Java package | MyBatis Mapper |
| 代码生成模板 | `yudao-module-infra/src/main/resources/codegen/sql/` | template | 代码生成 SQL 模板 |

## 命名与定位规则

- 表映射类以 `DO` 结尾。
- Mapper 类以 `Mapper` 结尾。
- XML Mapper 默认放在模块 `resources/mapper` 目录。
- SQL 按数据库类型分目录。
- 当前 MyBatis 类型别名配置见 `application.yaml` 中 `mybatis-plus.type-aliases-package`。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `sql/mysql/ruoyi-vue-pro.sql` | MySQL 初始化主脚本 | 当前最常用入口 |
| `sql/mysql/quartz.sql` | Quartz 表脚本 | Job 使用 JDBC 存储时需要 |
| `yudao-module-system/.../dal/dataobject/` | 系统模块 DO | 表映射定位 |
| `yudao-module-system/.../dal/mysql/` | 系统模块 Mapper | 查询入口定位 |
| `yudao-module-infra/src/main/resources/codegen/sql/` | SQL 生成模板 | 代码生成入口 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | 数据访问和缓存约束见 `tech-data-mybatis-cache.md` |
| `domain/feature/` | 功能流程落地后会引用具体表 |
| `domain/rule/` | 状态规则和权限规则会影响表字段设计 |

## 变更影响

SQL 脚本、DO、Mapper 或表结构变化会影响本地启动、代码生成、数据迁移、接口查询和权限过滤。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友采用的目标数据库 | 待确认 | 影响 SQL 维护主线 |
| 夸友业务表命名前缀 | 待确认 | 影响后续表结构规范 |
| 是否保留上游多租户字段 | 待确认 | 影响所有业务表 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |