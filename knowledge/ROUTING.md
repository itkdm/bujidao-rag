---
# 知识库基础设施文件
id: KB-INFRA-GLOBAL-ROUTING
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-17
tags:
- global
- routing
anchors:
- GLOBAL:ROUTING
---

# 路由规则

本文档是知识库的**需求级检索入口**。AI 在每个具体需求开始时，必须先读本文档进行定位。

> **注意**：`KNOWLEDGE-RULES.md` 是会话级初始化入口（首次接触知识库时读取），本文档是需求级检索入口（每个需求开始时读取）。两者分工不同，不要混淆。

## 路由顺序

1. 读取 `ROUTING.md`（本文档），根据需求线索定位目标目录。
2. 按路由结果进入对应目录，读取 `INDEX.md` 或应用总览。
3. 判断当前任务属于哪一层：
   - 全局业务概念、术语、规则 → `main/`
   - 应用或模块任务 → `applications/`
   - 上游官方材料、外部文章、证据核对 → `reference/`
   - 未确认推断或新发现 → `candidate/`
   - 个人经验或原始素材 → `personal/`
   - 写作结构约束模板 → `template/`
4. 只加载当前任务需要的最小知识文件集合。
5. 如果知识缺失或结论不确定，先写入 `candidate/`，不要直接创造稳定知识。
6. 如果 `feature/README.md` 标注当前无正式功能知识，不得自行脑补功能流程，应回到 `docs/` 或向 owner 确认。
7. **编码前必须回到当前仓库核对代码**。

## 路由提示

| 任务线索 | 优先读取 |
| --- | --- |
| 术语、角色、全局规则 | `main/` |
| 后端、前端、具体模块 | `applications/` |
| 上游官方文档、外部参考文章、证据核对 | `reference/` |
| 不确定推断、新发现 | `candidate/` |
| 排障、个人经验、碎片记录 | `personal/` |
| 新建知识文件、统一写法 | `template/` |

## 任务级最小读取路径

| 任务意图 | 最小读取路径 | 停止条件 |
| --- | --- | --- |
| 新增后端管理接口 | `applications/{appCode}/INDEX.md` → `base/README.md` → `base/base-api-index.md` → `rule/rule-permission-admin-app-boundary.md` → `tech/tech-framework-web-api.md` → `tech/tech-error-exception-log.md` | 已定位 Controller、权限边界、请求/响应规范、错误码规范 |
| 新增后端表或查询 | `applications/{appCode}/INDEX.md` → `base/base-database-index.md` → `base/base-model-index.md` → `tech/tech-data-mybatis-cache.md` | 已定位 SQL/DO/Mapper 规则和查询约束 |
| 新增后端定时任务或消息消费 | `applications/{appCode}/INDEX.md` → `base/base-async-index.md` → `tech/tech-async-job-mq.md` → `tech/tech-error-exception-log.md` | 已定位 Job/MQ 入口、异常处理和重试风险 |
| 判断上游模块能否直接复用 | `applications/{appCode}/INDEX.md` → `{appCode}.md` → `rule/rule-boundary-backend-baseline.md` → 必要时读取 `reference/` 对应证据 | 已确认模块启用状态、基线边界和待确认项 |
| 修改前端管理后台 | `applications/{appCode}/INDEX.md` → 对应 `base/README.md` 或 `rule/README.md` → `tech/README.md` | 已确认当前是否已有正式知识；没有则回到代码和候选知识 |
| 梳理产品功能或业务流程 | `docs/` → 必要时读取对应应用 `feature/README.md` | 已确认业务事实来自 docs 或人工确认，不把空 feature 当事实 |
| 写入新知识 | `KNOWLEDGE-RULES.md` → `template/` 对应模板 → 目标目录 README | 已确认知识类型、状态、owner、证据来源和目标路径 |

## 应用关键词路由

| 关键词 | 优先读取 |
| --- | --- |
| 后端、Java、Spring Boot、接口、数据库、权限 | `applications/{appCode}/INDEX.md` |
| 前端、管理后台、Vue3、Element Plus、用户管理 | `applications/{appCode}/INDEX.md` |
| 移动端、小程序、uni-app、H5 | `applications/{appCode}/INDEX.md` |

## 技术任务路由

| 任务线索 | 路由方式 |
| --- | --- |
| 架构约束、框架用法、事务、缓存、MQ、定时任务、异常、日志、权限、构建、测试、排障 | 先按应用关键词进入对应 `applications/{appCode}/INDEX.md`，再读取该应用的 `tech/README.md` |
| 无法判断属于哪个应用的通用技术约束 | 先查 `main/tech/`，没有稳定知识时写入 `candidate/` |
| 只是个人踩坑或一次性排查过程 | 写入 `personal/`，不要直接进入正式 `tech/` |

## 基础事实路由

| 任务线索 | 路由方式 |
| --- | --- |
| 模块、包结构、Controller、API、DO、VO、DTO、表、SQL、配置、权限编码、MQ、Job | 先按应用关键词进入对应 `applications/{appCode}/INDEX.md`，再读取该应用的 `base/README.md` |
| 需要知道"怎么实现、为什么这样实现" | 转到该应用的 `tech/README.md` |
| 需要了解功能能力、主要业务流程 | 转到该应用的 `feature/` |
| 需要了解业务规则、权限、状态约束、数据边界 | 转到该应用的 `rule/` |

## 规则知识路由

| 任务线索 | 路由方式 |
| --- | --- |
| 边界、权限、状态、数据可见性、安全例外、配置开关、合规追责 | 先按应用关键词进入对应 `applications/{appCode}/INDEX.md`，再读取该应用的 `rule/README.md` |
| 需要定位规则涉及的代码对象 | 转到该应用的 `base/README.md` |
| 需要实现规则对应代码 | 转到该应用的 `tech/README.md` |
| 全局协作规范（Git Commit、分支规范等） | `main/rules/` |

## 禁止事项

1. 不默认读取整个知识库。
2. 不在未 review 的情况下晋升候选知识。
3. 不把功能流程、业务规则、事实索引和技术约束混在同一个知识文件里。
4. 不把项目正式决策混进知识文件；已确认决策应进入 `docs/`。
5. 不将 DEPRECATED 知识作为正常路由结果返回（除非显式追溯历史）。