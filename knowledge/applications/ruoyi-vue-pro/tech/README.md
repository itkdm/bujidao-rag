---
id: KB-ENTRY-KUAYOU-RUOYI-VUE-PRO-TECH-INDEX
type: index
domain: kuayou
application: ruoyi-vue-pro
status: DRAFT
owner: bujidao
version: 2
updatedAt: 2026-08-09 15:55:00
---

# ruoyi-vue-pro 技术知识索引

本文档是 `ruoyi-vue-pro` 的 `tech/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体技术知识。

## 使用规则

1. 修改后端代码前，先判断任务属于哪个技术分类。
2. 只读取与当前任务相关的技术文档，避免全量加载。
3. 没有正式知识时，先查 `candidate/`，仍无法确认时回到代码事实。
4. 新增技术知识必须使用 `knowledge/template/tech-template.md`。

## 技术分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| architecture | 后端架构约束、模块边界、单体拆分边界、重要设计取舍 | `tech-architecture-{topic}.md` |
| framework | Spring Boot、yudao-framework、starter、目录约定、生命周期 | `tech-framework-{topic}.md` |
| api-integration | Controller、API 约定、外部系统调用、接口鉴权与兼容 | `tech-api-{topic}.md` |
| data-transaction | MyBatis、数据库、事务、缓存、幂等、一致性 | `tech-data-{topic}.md` |
| async-job | MQ、事件、定时任务、异步处理、WebSocket | `tech-async-{topic}.md` |
| error-observability | 异常处理、日志、监控、告警、排障入口 | `tech-error-{topic}.md` |
| security-permission | 登录鉴权、角色权限、租户、数据权限、安全边界 | `tech-security-{topic}.md` |
| build-env | Maven、JDK、Spring Profile、本地启动、部署配置 | `tech-build-{topic}.md` |
| testing-quality | 单元测试、集成测试、代码质量、质量门禁 | `tech-test-{topic}.md` |
| troubleshooting | 后端常见问题、启动失败、依赖冲突、数据库问题排查 | `tech-troubleshooting-{topic}.md` |

## 当前技术知识

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 模块边界与目录约束 | [tech-architecture-module-boundary.md](./tech-architecture-module-boundary.md) | DRAFT | 新增模块、判断代码层级、评估上游模块启用时读取 |
| Web API 与参数校验 | [tech-framework-web-api.md](./tech-framework-web-api.md) | DRAFT | 新增 Controller、ReqVO/RespVO、统一返回和校验时读取 |
| MyBatis 数据访问与缓存 | [tech-data-mybatis-cache.md](./tech-data-mybatis-cache.md) | DRAFT | 新增 DO、Mapper、分页查询、Redis 缓存时读取 |
| 权限、登录态与数据权限 | [tech-security-permission.md](./tech-security-permission.md) | DRAFT | 新增后台权限、判断数据权限、设计角色边界时读取 |
| 异常处理、错误码与日志 | [tech-error-exception-log.md](./tech-error-exception-log.md) | DRAFT | 新增业务异常、错误码、异常日志策略时读取 |
| 异步任务、定时任务与 Redis MQ | [tech-async-job-mq.md](./tech-async-job-mq.md) | DRAFT | 新增异步任务、Quartz Job、Redis MQ 消费链路时读取 |
| 本地构建与环境配置 | [tech-build-env-local.md](./tech-build-env-local.md) | DRAFT | 启动后端、调整 Maven/profile、排查构建环境时读取 |

## 常见任务路由

| 任务 | 优先读取 |
| --- | --- |
| 新增后端业务模块 | `tech-architecture-module-boundary.md` -> `tech-build-env-local.md` |
| 新增管理后台接口 | `tech-framework-web-api.md` -> `tech-security-permission.md` -> `tech-error-exception-log.md` |
| 新增数据库表和查询 | `tech-data-mybatis-cache.md` -> `tech-security-permission.md` |
| 新增业务错误码 | `tech-error-exception-log.md` |
| 新增定时任务或消息消费 | `tech-async-job-mq.md` -> `tech-error-exception-log.md` |
| 排查本地启动失败 | `tech-build-env-local.md` -> `tech-architecture-module-boundary.md` |
