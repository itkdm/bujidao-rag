---
# ==================== 必填字段 ====================
id: KB-TECH-KUAYOU-RUOYI-VUE-PRO-WEB-API
type: tech
scope: ruoyi-vue-pro
# 业务归属
domain: kuayou
application: ruoyi-vue-pro
appType: 后端应用

# 技术分类
techArea: framework
topic: web-api

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
    ref: ruoyi-vue-pro/yudao-framework/yudao-common/src/main/java/cn/iocoder/yudao/framework/common/pojo/CommonResult.java
    verifiedAt: 2026-08-09
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/01.新建模块.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/15.异常处理.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/16.参数校验.md

# 标签与锚点
tags:
  - backend
  - controller
  - api
  - validation
anchors:
  - APPLICATION:ruoyi-vue-pro
  - TECH_AREA:framework
  - TECH_TOPIC:web-api
---

# Web API 与参数校验约束

## AI 使用摘要

- 适用场景：新增 Controller、调整接口返回、编写 ReqVO/RespVO、处理参数校验时
- 关键入口：`DictTypeController`、`CommonResult`、`GlobalExceptionHandler`
- 关键规则：Controller 显式返回 `CommonResult<T>`；入参使用 VO + `@Valid`；管理后台接口使用 `controller.admin`，学生端接口使用 `controller.app`
- 关联知识：[tech-error-exception-log.md](./tech-error-exception-log.md)、[tech-security-permission.md](./tech-security-permission.md)
- 使用前必须核对：接口端类型、权限要求、返回 VO、校验注解、是否需要导出或特殊非 JSON 响应

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `DictTypeController.java` | 典型 CRUD Controller，包含 `@Validated`、`@Valid`、`CommonResult`、`@PreAuthorize` |
| code | `CommonResult.java` | 统一响应对象 |
| doc | `01.新建模块.md` | 官方新建 RESTful API 示例 |
| doc | `15.异常处理.md` | 官方说明为什么显式返回 `CommonResult` |
| doc | `16.参数校验.md` | 官方说明 `@Validated`、`@Valid` 和校验注解用法 |

## 适用范围

适用于 `ruoyi-vue-pro` 后端 HTTP API，包括管理后台 API、学生端/小程序 API、导出接口和普通查询接口。

## 不适用范围

第三方回调、文件下载、Excel 导出等不一定返回 `CommonResult` 的接口，需要按实际协议处理。

## 核心结论

- Controller 类使用 `@RestController`、`@RequestMapping`、`@Validated`。
- 成功响应优先返回 `CommonResult<T>`，并通过 `success(data)` 构造。
- Controller 入参不直接使用 DO；应使用 ReqVO，出参使用 RespVO。
- Bean 入参使用 `@Valid @RequestBody`；Query 参数对象使用 `@Valid`；单个参数按需使用 `@RequestParam` 和校验注解。
- 管理后台接口通常放在 `controller.admin`，用户端接口放在 `controller.app`，两者 VO 不混用。
- 分页接口使用项目封装的 `PageParam` / `PageResult`。

## 背景与约束

官方异常处理文档明确项目没有使用 `@ControllerAdvice` 自动包装 Controller 返回值，而是让方法签名显式返回 `CommonResult`。这样 Swagger/OpenAPI 展示和方法定义一致，也允许第三方回调等接口返回非标准结构。

`DictTypeController` 体现了当前代码风格：

- `@Tag`、`@Operation`、`@Parameter` 维护接口文档。
- `@PreAuthorize` 声明管理后台权限。
- `@Valid` 触发参数校验。
- `BeanUtils.toBean(...)` 做 DO 到 VO 的转换。
- Excel 导出直接写入 `HttpServletResponse`，不返回 `CommonResult`。

## 标准做法

新增普通管理后台 CRUD 接口时，推荐结构：

```java
@RestController
@RequestMapping("/system/example")
@Validated
public class ExampleController {

    @Resource
    private ExampleService exampleService;

    @PostMapping("/create")
    @PreAuthorize("@ss.hasPermission('system:example:create')")
    public CommonResult<Long> createExample(@Valid @RequestBody ExampleSaveReqVO reqVO) {
        return success(exampleService.createExample(reqVO));
    }
}
```

VO 使用建议：

| 类型 | 用途 |
| --- | --- |
| `SaveReqVO` | 创建/更新入参 |
| `PageReqVO` | 分页查询入参，继承或组合分页字段 |
| `RespVO` | 详情/列表返回 |
| `SimpleRespVO` | 下拉框、轻量列表 |

## 禁止或谨慎做法

- 禁止 Controller 直接返回 DO 给前端。
- 禁止 Controller 内写业务规则、数据库查询或复杂编排。
- 禁止无理由省略 `@Validated`、`@Valid` 和校验注解。
- 谨慎使用 `Map` 作为返回数据；优先定义明确 VO。
- 谨慎让 admin/app 共用同一个 VO，除非字段和安全边界完全一致。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| Controller 示例 | `yudao-module-system/.../DictTypeController.java` | CRUD API 风格参考 |
| 统一响应 | `yudao-framework/yudao-common/.../CommonResult.java` | API 响应结构 |
| 全局异常 | `yudao-framework/yudao-spring-boot-starter-web/.../GlobalExceptionHandler.java` | 参数错误、业务异常、系统异常统一转响应 |
| 官方校验文档 | `16.参数校验.md` | `@Validated`、`@Valid` 用法 |

## 变更影响与检查清单

- [ ] 新增接口前确认是 admin 端还是 app 端。
- [ ] Controller 方法返回类型是否为 `CommonResult<T>`，特殊响应是否有协议依据。
- [ ] 入参是否使用 ReqVO，并添加必要校验。
- [ ] 出参是否使用 RespVO，而非 DO。
- [ ] 管理后台接口是否有 `@PreAuthorize` 或明确免权限理由。
- [ ] 是否需要补充 OpenAPI 注解。

## 常见问题与踩坑

- Swagger 响应不准确：常见原因是没有显式使用 `CommonResult<T>`。
- 参数校验不生效：常见原因是缺少类上的 `@Validated` 或参数上的 `@Valid`。
- app 端泄露后台字段：常见原因是 admin/app 复用 VO。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友学生端 API 前缀是否沿用 `app-api` | 待确认 | 影响小程序端接口设计 |
| 夸友是否需要统一扩展响应字段 | 待确认 | 影响 `CommonResult` 是否保持上游结构 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |