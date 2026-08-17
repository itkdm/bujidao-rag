---
# ==================== 必填字段 ====================
id: KB-TECH-KUAYOU-RUOYI-VUE-PRO-SECURITY-PERMISSION
type: tech
scope: ruoyi-vue-pro
# 业务归属
domain: kuayou
application: ruoyi-vue-pro
appType: 后端应用

# 技术分类
techArea: security-permission
topic: permission

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
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-security/src/main/java/cn/iocoder/yudao/framework/security/core/service/SecurityFrameworkServiceImpl.java
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-biz-data-permission/src/main/java/cn/iocoder/yudao/framework/datapermission/core/annotation/DataPermission.java
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/dict/DictTypeController.java
    verifiedAt: 2026-08-09
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/07.功能权限.md
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/08.数据权限.md

# 标签与锚点
tags:
  - backend
  - security
  - permission
  - data-permission
anchors:
  - APPLICATION:ruoyi-vue-pro
  - TECH_AREA:security-permission
  - TECH_TOPIC:permission
---

# 权限、登录态与数据权限约束

## AI 使用摘要

- 适用场景：新增管理后台接口、判断是否需要 `@PreAuthorize`、处理数据权限过滤、设计角色权限时
- 关键入口：`@PreAuthorize`、`SecurityFrameworkServiceImpl`、`@DataPermission`
- 关键规则：管理后台接口一般要加功能权限；数据权限默认开启；禁用数据权限必须写清楚原因
- 关联知识：[tech-framework-web-api.md](./tech-framework-web-api.md)、[tech-data-mybatis-cache.md](./tech-data-mybatis-cache.md)
- 使用前必须核对：接口端类型、菜单权限编码、角色模型、是否受租户和数据权限影响

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `DictTypeController.java` | 管理后台接口使用 `@PreAuthorize("@ss.hasPermission(...)")` |
| code | `SecurityFrameworkServiceImpl.java` | `@ss` 权限判断最终委托权限 API |
| code | `DataPermission.java` | 数据权限默认开启，可通过注解控制 |
| doc | `07.功能权限.md` | 官方说明 RBAC、Token、`@PreAuthorize` |
| doc | `08.数据权限.md` | 官方说明数据权限实现和 `@DataPermission` |

## 适用范围

适用于管理后台接口权限、学生端/小程序登录态判断、数据权限、角色权限、租户相关安全边界。

## 不适用范围

不覆盖具体业务角色的产品定义，例如校园站长、楼栋主理人、学生用户的最终权限矩阵；这些应进入 `domain/rule/` 或正式产品文档。

## 核心结论

- 管理后台接口通常使用 `@PreAuthorize("@ss.hasPermission('module:resource:action')")`。
- 官方文档提示：一般情况下，管理后台接口使用 `@PreAuthorize`，用户 App 接口不使用后台菜单权限注解。
- `@ss.hasPermission(...)`、`hasRole(...)`、`hasScope(...)` 由 `SecurityFrameworkServiceImpl` 执行。
- 数据权限默认开启，不加 `@DataPermission` 也会生效。
- 需要忽略数据权限时使用 `@DataPermission(enable = false)`，但必须有明确原因。
- Token 认证与 OAuth2 令牌、Redis 缓存相关，不能绕过框架自行解析登录态。

## 背景与约束

功能权限基于 RBAC 模型，管理后台权限和菜单关联。典型 Controller 方法：

```java
@PreAuthorize("@ss.hasPermission('system:dict:create')")
public CommonResult<Long> createDictType(...) {}
```

数据权限通过 MyBatis 拦截实现，默认启用。当前代码中已有 `@DataPermission(enable = false)` 的使用场景，例如为了避免过滤导致无法查询用户或部门。

## 标准做法

新增管理后台接口时：

| 操作 | 权限编码建议 |
| --- | --- |
| 新增 | `{module}:{resource}:create` |
| 修改 | `{module}:{resource}:update` |
| 删除 | `{module}:{resource}:delete` |
| 查询 | `{module}:{resource}:query` |
| 导出 | `{module}:{resource}:export` |

判断是否禁用数据权限：

1. 是否会因为当前用户数据范围导致查不到自身必要信息。
2. 是否是系统级配置、字典、公共资源。
3. 禁用后是否可能越权暴露业务数据。
4. 是否有更小范围的 `includeRules` / `excludeRules` 替代。

## 禁止或谨慎做法

- 禁止管理后台敏感接口无权限注解且无说明。
- 禁止在业务代码中硬编码“超级管理员绕过”逻辑。
- 禁止为了修复查询为空就随意加 `@DataPermission(enable = false)`。
- 谨慎把后台权限模型直接套到学生端。
- 谨慎复用上游角色、租户和菜单配置，必须先匹配夸友组织模型。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| 权限判断 | `SecurityFrameworkServiceImpl` | `@ss` 权限表达式后端实现 |
| 功能权限示例 | `DictTypeController.java` | `@PreAuthorize` 示例 |
| 数据权限注解 | `DataPermission.java` | 启用/禁用/包含/排除数据权限规则 |
| 数据权限 starter | `yudao-spring-boot-starter-biz-data-permission` | 数据权限拦截器和规则 |

## 变更影响与检查清单

- [ ] 管理后台新增接口是否配置了权限编码。
- [ ] 权限编码是否和菜单/按钮权限保持一致。
- [ ] 查询接口是否受数据权限影响。
- [ ] 禁用数据权限是否有明确注释和安全评估。
- [ ] app 端接口是否需要登录态，但不应误用后台菜单权限。
- [ ] 多租户配置是否影响当前表和查询。

## 常见问题与踩坑

- 接口 403：可能是用户没有菜单权限，也可能是 `@PreAuthorize` 权限编码和菜单配置不一致。
- 查询结果缺失：可能是数据权限或租户过滤生效。
- 忽略数据权限后越权：禁用注解应只用于明确的系统级或自身信息查询场景。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友角色模型是否沿用上游 RBAC | 待确认 | 影响菜单权限、按钮权限和数据权限 |
| 校园站长/楼栋主理人是否映射为部门数据权限 | 待确认 | 影响数据范围实现 |
| 学生端是否单独设计权限体系 | 待确认 | 影响 app API 登录与鉴权方式 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |