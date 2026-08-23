---
id: KB-TECH-RUOYI-VUE-PRO-MODULE-BOUNDARY
type: tech
scope: app
appCode: ruoyi-vue-pro
status: DRAFT
owner: bujidao
maintainers:
- bujidao
version: 3
updatedAt: 2026-08-23
verifiedAt: 2026-08-09
confidence: high
stability: evolving
evidence:
- type: code
  ref: ruoyi-vue-pro/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java
- type: code
  ref: ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/02.后端手册/01.新建模块.md
tags:
- backend
- architecture
- module-boundary
- ruoyi-vue-pro
anchors:
- APP:RUOYI-VUE-PRO
- TECH:ARCHITECTURE
---

# 后端模块边界与目录约束

## AI 使用摘要

- 适用场景：新增后端模块、判断代码应放在哪一层、评估是否启用上游模块、调整模块依赖时
- 关键入口：`ruoyi-vue-pro/pom.xml`、`yudao-server/YudaoServerApplication.java`、各 `yudao-module-xxx/src/main/java`
- 关键规则：当前示例根工程聚合 `dependencies/framework/server/system/infra`，启动模块依赖 `system/infra`；模块内按 `controller/service/dal/api/mq/job/enums` 分层；目录存在不等于目标项目已采用该模块
- 关联知识：[ruoyi-vue-pro.md](../ruoyi-vue-pro.md)、[tech-build-env-local.md](./tech-build-env-local.md)
- 使用前必须核对：根 `pom.xml` 的 `<module>` 状态、启动类扫描包、目标模块是否已加入依赖

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | 确认当前 Maven 根工程聚合模块 |
| code | `yudao-server/pom.xml` | 确认当前启动模块实际依赖 |
| code | `YudaoServerApplication.java` | 确认启动类通过 `${yudao.info.base-package}.server` 和 `.module` 扫描 |
| code | `yudao-module-system/src/main/java/.../system/` | 确认实际模块内分层结构 |
| doc | `09.项目结构.md` | 官方说明 `yudao-dependencies`、`yudao-framework`、`yudao-module-xxx`、`yudao-server` 的职责 |
| doc | `01.新建模块.md` | 官方说明新建模块、添加依赖、接入 RESTful API 的流程 |

## 适用范围

本文适用于 `ruoyi-vue-pro/` 后端应用的模块划分、目录职责、代码放置位置、上游模块启用判断。

## 不适用范围

本文不决定目标项目是否复用任何上游可选模块；这类项目级取舍需要进入对应 Change 或 `rule/` 后再反向影响技术实现。

## 核心结论

- 当前 `ruoyi-vue-pro` 是单体后端工程，根 `pom.xml` 管理聚合构建边界，`yudao-server/pom.xml` 管理启动装配依赖。
- 当前根工程聚合：`yudao-dependencies`、`yudao-framework`、`yudao-server`、`yudao-module-system`、`yudao-module-infra`；其中启动模块依赖 `system` 与 `infra`。
- 其他可选模块即使目录存在，只要未参与根工程聚合或未被启动模块依赖，就不能描述为当前运行已采用。
- 新增项目代码时，优先新增职责清晰的独立模块或在明确复用的上游模块中扩展，不能把实现散落到 `yudao-server`。
- 模块内职责分层应遵守：`controller` 负责端口 API，`service` 负责业务逻辑，`dal` 负责数据访问，`api` 负责模块间能力暴露，`mq/job` 负责异步和定时入口，`enums` 负责枚举与错误码。

## 背景与约束

官方文档说明 `ruoyi-vue-pro` 本质是单体项目，但通过多个 `yudao-module-xxx` Maven 模块管理能力。任何目标项目启用、裁剪或扩展模块前，都要先基于当前代码完成边界评估。

启动类 `YudaoServerApplication` 使用：

```java
@SpringBootApplication(scanBasePackages = {"${yudao.info.base-package}.server", "${yudao.info.base-package}.module"})
```

这意味着新模块包名必须落在 `${yudao.info.base-package}.module` 下，否则不会被默认扫描。

## 标准做法

新增后端能力时，先判断能力类型：

| 能力类型 | 推荐位置 |
| --- | --- |
| 新业务域能力 | 新建或确认一个 `yudao-module-{biz}` 模块 |
| 管理后台 API | `controller.admin` |
| App 端/客户端 API | `controller.app` |
| 业务编排与规则校验 | `service` / `service.impl` |
| 数据库访问 | `dal.dataobject` + `dal.mysql` |
| Redis 缓存访问 | `dal.redis` |
| 跨模块调用能力 | `api` + 实现类 |
| 异步消息 | `mq.message` + `mq.producer` + `mq.consumer` |
| 定时任务 | `job` |
| 错误码和枚举 | `enums` |

新增 Maven 模块时，至少检查：

- 根 `pom.xml` 是否添加 `<module>`。
- `yudao-server/pom.xml` 是否引入目标模块依赖。
- 包名是否在 `cn.iocoder.yudao.module.{module}` 下。
- 数据库脚本、菜单权限、配置项是否独立维护。

## 禁止或谨慎做法

- 禁止把项目实现直接塞进 `yudao-server`，它应保持启动和装配入口职责。
- 禁止仅因为目录存在或根工程已聚合就认为模块进入运行，必须同时核对根 `pom.xml`、`yudao-server/pom.xml` 和相关配置。
- 谨慎直接修改 `yudao-framework`，除非是全局技术能力；业务差异不应下沉到 framework。
- 谨慎复用任何上游可选模块，必须先评估模型、数据库、菜单、接口和目标项目需求是否匹配。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| 根工程 | `ruoyi-vue-pro/pom.xml` | 判断模块是否参与聚合构建 |
| 启动模块依赖 | `yudao-server/pom.xml` | 判断模块是否进入当前启动装配 |
| 启动类 | `yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java` | 判断扫描范围 |
| 系统模块 | `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/` | 参考标准模块结构 |
| 基础设施模块 | `yudao-module-infra/` | 任务、代码生成、文件、配置等基础能力 |
| 框架层 | `yudao-framework/` | 通用 starter 和全局技术能力 |

## 变更影响与检查清单

- [ ] 修改模块启用状态前，核对根 `pom.xml`、`yudao-server/pom.xml`、数据库脚本和配置项。
- [ ] 新增模块前，确认包名能被启动类扫描。
- [ ] 新增业务代码前，判断应进入 `controller/service/dal/api/mq/job/enums` 哪一层。
- [ ] 启用上游业务模块前，先评估是否会引入未使用表、菜单、定时任务、MQ 消费者。
- [ ] 修改 `yudao-framework` 前，确认不是单个业务模块的局部需求。

## 常见问题与踩坑

- 目录存在但未参与聚合：根 `pom.xml` 注释掉的模块不会参与当前聚合构建；是否进入运行还需核对启动模块依赖与配置。
- 接口 404：常见原因是模块未被引入、包名不在扫描范围、Controller 路径或 API 前缀不符合配置。
- 业务代码放错层：Service 中应聚焦业务逻辑，Mapper 查询应沉到 `dal.mysql`，缓存访问应沉到 `dal.redis`。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 目标项目是否新建独立模块 | 待初始化 | 影响后端模块边界和包名 |
| 目标项目启用哪些上游模块 | 待初始化 | 影响依赖、数据模型和接口边界 |
| 是否保留上游多租户能力 | 待确认 | 影响数据权限、租户字段和后台组织模型 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 3 | 2026-08-23 | 移除具体业务耦合，并校准模块聚合与运行装配边界 | Codex |
