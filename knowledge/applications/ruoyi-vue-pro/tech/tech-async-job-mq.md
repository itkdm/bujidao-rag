---
id: KB-TECH-RUOYI-VUE-PRO-ASYNC-JOB-MQ
type: tech
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

# 证据
evidence:
  - type: code
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-job/src/main/java/cn/iocoder/yudao/framework/quartz/core/handler/JobHandler.java
  - type: code
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-mq/src/main/java/cn/iocoder/yudao/framework/mq/redis/core/RedisMQTemplate.java
  - type: code
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-mq/src/main/java/cn/iocoder/yudao/framework/mq/redis/core/stream/AbstractRedisStreamMessageListener.java
  - type: code
    ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/job/token/TokenCleanJob.java
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/30.异步任务.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/03.中间件手册/06.定时任务.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/03.中间件手册/12.消息队列（Redis）.md

# 标签与锚点
tags:
  - backend
  - async
  - job
  - mq
  - redis-stream
anchors:
  - APP:RUOYI-VUE-PRO
  - TECH:ASYNC-JOB-MQ
---

# 异步任务、定时任务与 Redis MQ 约束

## AI 使用摘要

- 适用场景：新增后台异步处理、定时任务、短信/通知/库存等消息消费链路时
- 关键入口：`@Async`、`JobHandler`、`RedisMQTemplate`、`AbstractRedisStreamMessageListener`
- 关键规则：短时非关键异步可用 Spring Async；可管理定时任务用 Quartz `JobHandler`；可靠可堆积消息优先评估 Redis Stream，但失败重试和幂等需单独设计
- 关联知识：[tech-error-exception-log.md](./tech-error-exception-log.md)、[tech-data-mybatis-cache.md](./tech-data-mybatis-cache.md)
- 使用前必须核对：是否需要持久化、是否允许丢失、是否需要重试、是否要求幂等、是否涉及事务提交后发送

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `JobHandler.java` | Quartz Job 接入接口 |
| code | `TokenCleanJob.java` | 系统模块定时任务示例 |
| code | `RedisMQTemplate.java` | Redis pub/sub 与 Stream 发送入口 |
| code | `AbstractRedisStreamMessageListener.java` | Redis Stream 集群消费监听器，包含失败重试/幂等等 TODO |
| doc | `30.异步任务.md` | 官方 Spring Async 说明 |
| doc | `06.定时任务.md` | 官方 Quartz Job 说明 |
| doc | `12.消息队列（Redis）.md` | 官方 Redis MQ 集群/广播消费说明 |

## 适用范围

适用于后端异步执行、Quartz 定时任务、Redis MQ 消息生产消费、任务幂等和重试设计。

## 不适用范围

不覆盖 RocketMQ/RabbitMQ/Kafka 的具体生产配置；当前文档只基于已读官方 Redis MQ 文档和当前代码事实。

## 核心结论

- Spring Async 适合短时、非关键、允许 JVM 重启丢失的异步任务。
- Quartz Job 适合需要后台配置、执行日志、调度管理的定时任务。
- Redis Stream 适合可靠、可堆积、集群消费的异步任务，要求 Redis 5.0+。
- Redis pub/sub 适合广播消费，但不适合需要可靠堆积的任务。
- 当前 `AbstractRedisStreamMessageListener` 代码中对异常处理、消费日志、通用幂等、失败重试仍有 TODO，使用时必须额外设计。
- 消息发送与数据库事务结合时，必须考虑“事务回滚但消息已发出”的问题。

## 背景与约束

官方 Redis MQ 文档区分：

| 模式 | 技术 | 特点 |
| --- | --- | --- |
| 集群消费 | Redis Stream | 一个消息只被一个消费者实例消费，可堆积 |
| 广播消费 | Redis pub/sub | 每个实例都能收到，但不可靠堆积 |

当前框架提供 `RedisMQTemplate#send(...)` 发送消息，Stream 消费者继承 `AbstractRedisStreamMessageListener<T>`。但监听器代码里明确留下失败重试、幂等、日志、事务结合的 TODO。

## 标准做法

选择异步技术：

| 需求 | 推荐方式 |
| --- | --- |
| 写日志、轻量通知、可丢失 | `@Async` |
| 每日/定时清理、同步任务 | Quartz `JobHandler` |
| 短信、站内信、通知等需堆积任务 | Redis Stream |
| 多实例都要收到配置变更 | Redis pub/sub |

新增 Job：

```java
@Component
public class ExampleJob implements JobHandler {
    @Override
    public String execute(String param) throws Exception {
        return "执行结果";
    }
}
```

新增 Redis Stream 消息链路：

1. 定义 Message，继承 `AbstractRedisStreamMessage`。
2. Producer 注入 `RedisMQTemplate` 并发送消息。
3. Consumer 继承 `AbstractRedisStreamMessageListener<Message>`。
4. Consumer 内部必须保证业务幂等。
5. 失败重试和异常告警必须按业务风险单独设计。

## 禁止或谨慎做法

- 禁止把关键业务一致性依赖在普通 `@Async` 上。
- 禁止假设 Redis Stream 当前封装已经自动完成通用幂等和失败重试。
- 禁止在事务未提交前发送会影响外部状态的消息，除非有补偿设计。
- 谨慎在 Job 中一次性处理大量数据，应限制批量大小。
- 谨慎在本地环境默认开启所有 Job，避免误改数据。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| 异步配置 | `YudaoAsyncAutoConfiguration` | Spring Async 线程池配置 |
| Job 接口 | `JobHandler` | 定时任务业务入口 |
| Job 示例 | `TokenCleanJob` | 令牌清理任务 |
| Redis MQ 发送 | `RedisMQTemplate` | pub/sub 与 Stream 发送 |
| Stream 消费 | `AbstractRedisStreamMessageListener` | 集群消费监听 |
| 系统 MQ 示例 | `system/mq/producer`、`system/mq/consumer`、`system/mq/message` | 邮件、短信消息链路 |

## 变更影响与检查清单

- [ ] 任务是否允许丢失。
- [ ] 是否需要执行日志和后台调度管理。
- [ ] 是否需要多实例集群消费或广播消费。
- [ ] 消费是否具备业务幂等。
- [ ] 失败是否需要重试、告警或人工补偿。
- [ ] 消息发送是否在事务提交后进行。
- [ ] 本地/测试/生产环境 Job 开关是否正确。

## 常见问题与踩坑

- JVM 重启导致异步任务丢失：不要用 `@Async` 承载关键任务。
- 消息重复消费：Redis Stream 场景仍应做业务幂等。
- Job 执行压垮数据库：参考 `TokenCleanJob` 使用批量限制。
- 本地误跑任务：注意 `application-local.yaml` 中 Quartz 自动配置和开关。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友订单/库存异步链路使用 Redis Stream 还是外部 MQ | 待确认 | 影响可靠性、重试和运维成本 |
| 是否需要统一消息幂等表 | 待确认 | 影响消费一致性 |
| 本地开发是否默认关闭业务 Job | 待确认 | 影响调试和数据安全 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |