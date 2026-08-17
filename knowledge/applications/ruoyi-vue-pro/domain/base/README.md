---
id: KB-ENTRY-KUAYOU-RUOYI-VUE-PRO-BASE-INDEX
type: index
domain: kuayou
application: ruoyi-vue-pro
status: DRAFT
owner: bujidao
version: 2
updatedAt: 2026-08-09 15:55:00
---

# ruoyi-vue-pro 基础事实索引

本文档是 `ruoyi-vue-pro` 的 `domain/base/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体事实索引。

## 使用规则

1. `base/` 只记录事实入口，不解释实现方案。
2. 修改代码前，如果需要定位模块、接口、模型、表、配置、权限、消息或任务，先读本文件。
3. 需要了解“怎么实现、为什么这样实现”，转到 `tech/`。
4. 需要了解业务流程，先读 `domain/feature/README.md`；当前无正式 feature 知识时，回到 `docs/01-product/` 或向布吉岛确认。
5. 需要了解业务规则，转到 `domain/rule/`。
6. 新增基础事实索引必须使用 `knowledge/template/base-template.md`。

## 基础分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| module | 模块、包结构、启用状态、核心路径 | `base-module-{topic}.md` |
| api | Controller、API 前缀、接口入口、接口文档 | `base-api-{topic}.md` |
| model | DO、ReqVO、RespVO、DTO、Enum、ErrorCode | `base-model-{topic}.md` |
| database | SQL、表、字段、索引、逻辑删除、Quartz 表 | `base-database-{topic}.md` |
| config | YAML、profile、环境变量、中间件配置 | `base-config-{topic}.md` |
| permission | 权限编码、角色、菜单、数据权限入口 | `base-permission-{topic}.md` |
| async | MQ、Message、Producer、Consumer、Job | `base-async-{topic}.md` |

## 当前基础索引

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 模块与包结构索引 | [base-module-index.md](./base-module-index.md) | DRAFT | 定位当前启用模块、未启用模块、标准包结构 |
| API 入口索引 | [base-api-index.md](./base-api-index.md) | DRAFT | 定位 admin/app Controller、API 前缀、接口文档入口 |
| 模型对象索引 | [base-model-index.md](./base-model-index.md) | DRAFT | 定位 DO、VO、DTO、Enum、ErrorCode |
| 数据库与 SQL 索引 | [base-database-index.md](./base-database-index.md) | DRAFT | 定位 SQL 脚本、表结构入口、Quartz SQL |
| 配置入口索引 | [base-config-index.md](./base-config-index.md) | DRAFT | 定位 application 配置、profile、中间件配置 |
| 权限事实索引 | [base-permission-index.md](./base-permission-index.md) | DRAFT | 定位权限注解、权限 API、数据权限入口 |
| 异步与任务索引 | [base-async-index.md](./base-async-index.md) | DRAFT | 定位 MQ、Message、Producer、Consumer、Job |

## 常见任务路由

| 任务 | 优先读取 |
| --- | --- |
| 判断代码放在哪个模块 | `base-module-index.md` |
| 找某类接口入口 | `base-api-index.md` |
| 找请求/响应/数据库对象 | `base-model-index.md` |
| 找 SQL 或表结构入口 | `base-database-index.md` |
| 找本地环境或中间件配置 | `base-config-index.md` |
| 找权限编码和数据权限入口 | `base-permission-index.md` |
| 找 MQ 或 Job 入口 | `base-async-index.md` |
