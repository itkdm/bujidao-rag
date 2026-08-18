---
id: KB-TECH-RUOYI-VUE-PRO-EXCEPTION-LOG
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
evidence:
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-web/src/main/java/cn/iocoder/yudao/framework/web/core/handler/GlobalExceptionHandler.java
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-common/src/main/java/cn/iocoder/yudao/framework/common/exception/util/ServiceExceptionUtil.java
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/enums/ErrorCodeConstants.java
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/15.异常处理.md
tags:
- backend
- exception
- error-code
- log
anchors:
- APP:RUOYI-VUE-PRO
- TECH:EXCEPTION-LOG
---

# 异常处理、错误码与日志约束

## AI 使用摘要

- 适用场景：新增业务异常、定义错误码、处理参数错误、调整异常日志记录时
- 关键入口：`GlobalExceptionHandler`、`ServiceExceptionUtil`、各模块 `ErrorCodeConstants`
- 关键规则：业务失败用 `ServiceException` 抛出；错误码按模块集中定义；系统异常由全局处理器记录错误日志并返回通用失败
- 关联知识：[tech-framework-web-api.md](./tech-framework-web-api.md)
- 使用前必须核对：错误码段是否冲突、异常是否会触发事务回滚、是否会被全局异常处理器捕获

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `GlobalExceptionHandler.java` | 将 MVC、校验、权限、业务、系统异常转换成 `CommonResult` |
| code | `ServiceExceptionUtil.java` | 业务异常构造工具 |
| code | `system/enums/ErrorCodeConstants.java` | 系统模块错误码集中定义 |
| doc | `15.异常处理.md` | 官方说明统一响应、业务异常和错误码设计 |

## 适用范围

适用于后端业务异常、参数异常、权限异常、系统异常、错误码定义和 API 错误日志。

## 不适用范围

不覆盖前端错误展示文案策略，也不覆盖第三方接口回调要求的特殊响应格式。

## 核心结论

- Controller 成功返回 `CommonResult.success(...)`；业务失败不要返回失败对象，应在 Service 层抛出 `ServiceException`。
- 业务异常通过 `ServiceExceptionUtil.exception(ErrorCode, params...)` 创建。
- 错误码应集中在模块的 `enums/ErrorCodeConstants.java` 中维护。
- `GlobalExceptionHandler` 会处理参数错误、权限不足、业务异常、系统异常，并统一返回 `CommonResult`。
- 系统异常会记录 `ApiErrorLog`，包含 traceId、用户、请求、异常栈等信息。
- 业务异常通常按 warn 级别处理，避免大量堆栈污染日志。

## 背景与约束

官方文档明确推荐业务异常走抛异常方式，而不是返回失败 `CommonResult`。原因之一是 Spring 声明式事务基于异常回滚；如果用返回值表达失败，事务处理会变复杂。

当前代码中的 `GlobalExceptionHandler` 对异常进行了分层：

| 异常类型 | 处理结果 |
| --- | --- |
| 参数缺失、类型错误、校验失败 | 返回 `BAD_REQUEST` |
| `AccessDeniedException` | 返回 `FORBIDDEN` |
| `ServiceException` | 返回业务错误码和消息 |
| 其他系统异常 | 记录 API 错误日志，返回 `INTERNAL_SERVER_ERROR` |

## 标准做法

新增业务错误码：

```java
ErrorCode EXAMPLE_NOT_EXISTS = new ErrorCode(1_002_999_000, "示例不存在");
```

Service 层抛出业务异常：

```java
if (example == null) {
    throw exception(EXAMPLE_NOT_EXISTS);
}
```

错误码命名建议：

| 场景 | 命名 |
| --- | --- |
| 数据不存在 | `{OBJECT}_NOT_EXISTS` |
| 状态不允许 | `{OBJECT}_STATUS_INVALID` |
| 唯一性冲突 | `{OBJECT}_DUPLICATE` |
| 子资源存在无法删除 | `{OBJECT}_HAS_CHILDREN` |

## 禁止或谨慎做法

- 禁止在 Controller 中拼业务失败响应，业务规则失败应由 Service 抛出异常。
- 禁止在多个类里散落定义错误码。
- 禁止复用语义不准确的错误码，只为省一个常量。
- 谨慎捕获异常后吞掉，除非有明确补偿或降级策略。
- 谨慎在业务异常中输出敏感信息。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| 全局异常处理 | `GlobalExceptionHandler` | 统一异常转响应和错误日志 |
| 业务异常工具 | `ServiceExceptionUtil` | 构造 `ServiceException` |
| 业务异常类 | `ServiceException` | 携带错误码和消息 |
| 全局错误码 | `GlobalErrorCodeConstants` | 系统级错误 |
| 模块错误码 | `module/{module}/enums/ErrorCodeConstants.java` | 业务模块错误 |

## 变更影响与检查清单

- [ ] 新增错误码是否落在正确模块。
- [ ] 错误码编号是否与已有编号冲突。
- [ ] Service 失败是否抛异常而不是返回失败对象。
- [ ] 异常文案是否适合直接展示给用户。
- [ ] 是否存在敏感信息进入日志或响应。
- [ ] 事务方法中的异常是否能正确触发回滚。

## 常见问题与踩坑

- 事务没有回滚：常见原因是用返回值表达失败，或捕获异常后没有重新抛出。
- 错误码难维护：常见原因是没有按模块集中维护。
- 日志过多：业务异常不应都按 error 打印完整堆栈。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友新增业务模块的错误码段 | 待确认 | 影响后续错误码编号规范 |
| 夸友对用户端错误文案是否有统一风格 | 待确认 | 影响错误码消息是否直接面向用户 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |