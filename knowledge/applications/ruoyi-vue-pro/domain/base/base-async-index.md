---
id: KB-BASE-RUOYI-VUE-PRO-ASYNC
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
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/mq/
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/job/
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-mq/
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-job/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/03.中间件手册/06.定时任务.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/03.中间件手册/12.消息队列（Redis）.md
tags:
- backend
- async
- mq
- job
anchors:
- APP:RUOYI-VUE-PRO
- BASE:ASYNC
---

# 异步与任务索引

## AI 使用摘要

- 适用场景：定位 MQ 消息、生产者、消费者、Quartz Job、异步 starter 时
- 关键入口：`yudao-module-system/src/main/java/.../mq/`、`job/`
- 关键事实：system 模块已有邮件/短信 MQ 链路；Job 实现 `JobHandler`；Redis MQ 和 Quartz starter 位于 `yudao-framework`
- 关联知识：[tech-async-job-mq.md](../../tech/tech-async-job-mq.md)
- 使用前必须核对：当前功能是否启用、消息模式、Job 配置、是否需要幂等和重试

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `yudao-module-system/.../mq/` | 当前 MQ 示例入口 |
| code | `yudao-module-system/.../job/` | 当前 Job 示例入口 |
| code | `yudao-spring-boot-starter-mq/` | Redis MQ framework |
| code | `yudao-spring-boot-starter-job/` | Quartz Job framework |
| doc | `06.定时任务.md` | 官方 Job 说明 |
| doc | `12.消息队列（Redis）.md` | 官方 Redis MQ 说明 |

## 索引范围

本文索引异步消息、Redis MQ、Producer、Consumer、Message、Quartz Job 和相关 framework 入口。

## 不收录范围

本文不解释消息可靠性、幂等、失败重试等实现约束；这些见 `tech/tech-async-job-mq.md`。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| MQ 根路径 | `yudao-module-system/.../mq/` | Java package | system 模块消息入口 |
| Message | `mq/message/` | Java package | 邮件、短信消息对象 |
| Producer | `mq/producer/` | Java package | 邮件、短信、用户相关消息生产者 |
| Consumer | `mq/consumer/` | Java package | 邮件、短信消息消费者 |
| Job 根路径 | `yudao-module-system/.../job/` | Java package | system 模块定时任务入口 |
| Token 清理 Job | `job/token/TokenCleanJob.java` | Job | 清理 OAuth2 token 示例 |
| Redis MQ 模板 | `RedisMQTemplate.java` | Framework class | Redis 消息发送入口 |
| Stream Listener | `AbstractRedisStreamMessageListener.java` | Framework class | Redis Stream 集群消费监听器 |
| Job 接口 | `JobHandler.java` | Framework interface | Quartz Job 接入接口 |

## 命名与定位规则

- 消息对象通常放在 `mq/message`。
- 消息生产者通常放在 `mq/producer`。
- 消息消费者通常放在 `mq/consumer`。
- 定时任务类通常放在模块 `job` 包，并实现 `JobHandler`。
- Redis MQ framework 位于 `yudao-framework/yudao-spring-boot-starter-mq`。
- Quartz Job framework 位于 `yudao-framework/yudao-spring-boot-starter-job`。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `yudao-module-system/src/main/java/.../system/mq/` | 消息链路入口 | 邮件、短信示例 |
| `yudao-module-system/src/main/java/.../system/job/` | 定时任务入口 | DemoJob、TokenCleanJob |
| `yudao-framework/yudao-spring-boot-starter-mq/` | MQ framework | Redis/RabbitMQ 等 starter |
| `yudao-framework/yudao-spring-boot-starter-job/` | Job framework | Quartz 封装 |
| `sql/mysql/quartz.sql` | Quartz 表脚本 | JDBC JobStore 需要 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | 异步任务可靠性和幂等约束见 `tech-async-job-mq.md` |
| `domain/feature/` | 业务流程会引用具体消息或任务 |
| `domain/rule/` | 重试、补偿、通知规则应进入 rule |

## 变更影响

MQ 或 Job 入口变化会影响异步处理、后台任务、消息可靠性、数据库压力、本地启动和生产运维。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友订单/库存是否使用 MQ | 待确认 | 影响消息索引扩展 |
| 本地开发是否默认运行 Job | 待确认 | 影响调试和数据安全 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |