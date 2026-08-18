---
id: KB-TECH-RUOYI-VUE-PRO-MYBATIS-CACHE
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
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/mysql/dict/DictTypeMapper.java
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/dal/dataobject/dict/DictTypeDO.java
- type: code
  ref: ruoyi-vue-pro/yudao-framework/yudao-spring-boot-starter-mybatis/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/25.MyBatis 数据库.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/28.Redis 缓存.md
tags:
- backend
- mybatis
- database
- redis
- cache
anchors:
- APP:RUOYI-VUE-PRO
- TECH:MYBATIS-CACHE
---

# MyBatis 数据访问与缓存约束

## AI 使用摘要

- 适用场景：新增 DO、Mapper、分页查询、Redis 缓存、数据库访问逻辑时
- 关键入口：`BaseMapperX`、`LambdaQueryWrapperX`、`dal.dataobject`、`dal.mysql`、`dal.redis`
- 关键规则：MyBatis 操作只放 Mapper 层；DO 不作为 Controller 出入参；Redis Key 集中定义
- 关联知识：[tech-framework-web-api.md](./tech-framework-web-api.md)、[tech-error-exception-log.md](./tech-error-exception-log.md)
- 使用前必须核对：表结构、逻辑删除字段、租户字段、分页封装、缓存一致性策略

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `DictTypeDO.java` | DO 使用 `@TableName`、`@TableId`、继承 `BaseDO` |
| code | `DictTypeMapper.java` | Mapper 继承 `BaseMapperX` 并使用 `LambdaQueryWrapperX` |
| code | `yudao-spring-boot-starter-mybatis/` | MyBatis 增强封装 |
| doc | `25.MyBatis 数据库.md` | 官方数据访问规范 |
| doc | `28.Redis 缓存.md` | 官方 Redis Key 与 RedisDAO 约定 |

## 适用范围

适用于后端数据库实体、Mapper 查询、分页、逻辑删除、Redis 缓存访问和缓存 Key 管理。

## 不适用范围

不覆盖具体业务表设计和字段语义；这些应进入 `base/` 或正式数据库设计文档。

## 核心结论

- DO 放在 `dal.dataobject`，以 `DO` 结尾。
- Mapper 放在 `dal.mysql`，以 `Mapper` 结尾，并继承 `BaseMapperX<T>`。
- 查询条件优先使用 `LambdaQueryWrapperX` / `QueryWrapperX` 的 `xxxIfPresent` 方法。
- 禁止 Controller、Service 直接写 MyBatis Plus 查询细节，查询逻辑应沉到 Mapper。
- Mapper XML 默认放在模块 `resources/mapper` 目录。
- Redis Key 应集中定义在模块的 `RedisKeyConstants`，Redis 访问封装为 `RedisDAO`，不要在 Service 中散落拼 Key。

## 背景与约束

官方文档强调，禁止在 Controller、Service 中直接进行 MyBatis Plus 操作。原因是查询逻辑散落会让 Service 失去业务聚焦，也降低查询复用性。

当前 `DictTypeMapper` 体现了推荐写法：

```java
default PageResult<DictTypeDO> selectPage(DictTypePageReqVO reqVO) {
    return selectPage(reqVO, new LambdaQueryWrapperX<DictTypeDO>()
            .likeIfPresent(DictTypeDO::getName, reqVO.getName())
            .eqIfPresent(DictTypeDO::getStatus, reqVO.getStatus())
            .orderByDesc(DictTypeDO::getId));
}
```

## 标准做法

新增数据库对象时：

| 层 | 做法 |
| --- | --- |
| DO | `dal.dataobject.{biz}`，继承 `BaseDO`，标注 `@TableName` |
| Mapper | `dal.mysql.{biz}`，继承 `BaseMapperX<DO>` |
| 查询 | Mapper 默认方法封装条件，不在 Service 拼复杂查询 |
| 分页 | 返回 `PageResult<DO>`，Controller 再转为 `PageResult<RespVO>` |
| 缓存 | `dal.redis` 中封装 RedisDAO，Key 集中到 `RedisKeyConstants` |

缓存策略建议：

- 热点配置、Token、权限等可缓存。
- 业务强一致数据要先明确失效策略。
- 涉及事务提交后的缓存刷新，要避免“数据库回滚但缓存已更新”。

## 禁止或谨慎做法

- 禁止 Controller 直接注入 Mapper。
- 禁止 Service 内散落 `new LambdaQueryWrapperX` 做重复查询。
- 禁止把 DO 返回给前端。
- 禁止 Redis Key 字符串散落在 Service。
- 谨慎使用批量插入封装；官方文档说明 `BaseMapperX.insertBatch` 适合少量或性能要求不高的场景。
- 谨慎绕开逻辑删除、租户、数据权限相关拦截器。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| DO 示例 | `DictTypeDO.java` | 表映射对象 |
| Mapper 示例 | `DictTypeMapper.java` | 查询封装 |
| Mapper 基类 | `BaseMapperX` | 项目增强 CRUD |
| 条件构造器 | `LambdaQueryWrapperX` | `xxxIfPresent` 查询条件 |
| Redis Key 约定 | `RedisKeyConstants` | 模块缓存 Key 集中管理 |

## 变更影响与检查清单

- [ ] 新表是否有 DO、Mapper、必要索引和初始化 SQL。
- [ ] Mapper 查询是否可复用，是否避免 Service 拼查询。
- [ ] 分页是否使用项目 `PageResult`。
- [ ] 是否受租户/数据权限/逻辑删除影响。
- [ ] 缓存是否有明确 Key、TTL、失效或刷新策略。
- [ ] 写操作和缓存更新是否考虑事务边界。

## 常见问题与踩坑

- 查询条件误拼：优先使用 `xxxIfPresent`，避免空值进入条件。
- 缓存不一致：常见原因是写库和删缓存顺序没有结合事务边界。
- 删除后唯一索引冲突：上游部分表通过 `deleted_time` 等字段辅助逻辑删除唯一性。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友业务表命名前缀 | 待确认 | 影响 DO、Mapper 和 SQL 规范 |
| 是否保留上游逻辑删除和租户字段 | 待确认 | 影响所有业务表结构 |
| 缓存一致性策略 | 待确认 | 影响订单、库存、权限等高频数据 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |