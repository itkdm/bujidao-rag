---
id: KB-TECH-RUOYI-VUE-PRO-BUILD-ENV
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
  ref: ruoyi-vue-pro/pom.xml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/resources/application.yaml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/resources/application-local.yaml
- type: code
  ref: ruoyi-vue-pro/yudao-server/src/main/resources/application-dev.yaml
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/05.快速启动【后端】.md
- type: doc
  ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/08.技术选型.md
- type: doc
  ref: docs/06-tech/02-上游源码版本记录.md
tags:
- backend
- build
- maven
- jdk17
- local-env
anchors:
- APP:RUOYI-VUE-PRO
- TECH:BUILD-ENV
---

# 本地构建与环境配置约束

## AI 使用摘要

- 适用场景：启动后端、调整 Maven 模块、修改 profile、排查本地构建失败时
- 关键入口：根 `pom.xml`、`application.yaml`、`application-local.yaml`、`application-dev.yaml`
- 关键规则：当前基线是 `master-jdk17`；Java 版本为 17；当前启用模块以根 `pom.xml` 为准
- 关联知识：[tech-architecture-module-boundary.md](./tech-architecture-module-boundary.md)
- 使用前必须核对：本地数据库、Redis、Quartz、MQ、敏感配置、启用模块状态

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `ruoyi-vue-pro/pom.xml` | Java 17、Spring Boot 3.5.15、启用模块 |
| code | `application.yaml` | 全局配置、base-package、MyBatis、WebSocket 等 |
| code | `application-local.yaml` | 本地环境端口、数据源、Redis、Quartz、MQ |
| code | `application-dev.yaml` | 开发环境配置 |
| doc | `05.快速启动【后端】.md` | 官方后端快速启动说明 |
| doc | `08.技术选型.md` | 官方技术栈说明 |
| doc | `docs/06-tech/02-上游源码版本记录.md` | 夸友接入基线分支与 commit |

## 适用范围

适用于后端本地启动、Maven 构建、环境配置、profile 调整、依赖版本判断。

## 不适用范围

不覆盖生产部署方案，也不覆盖敏感配置的真实值管理；生产部署应进入正式运维文档。

## 核心结论

- 后端来源基线：`YunaiV/ruoyi-vue-pro` 的 `master-jdk17` 分支。
- 当前接入 commit：`ec3f7cbf73e88514a70a6b59d365092ee470603d`。
- 根 `pom.xml` 配置 Java 17、Spring Boot 3.5.15。
- 本地默认端口在 `application-local.yaml` / `application-dev.yaml` 中为 `48080`。
- `application.yaml` 中 `yudao.info.base-package` 当前为 `cn.iocoder.yudao`，影响启动类扫描和 MyBatis type aliases。
- 本地环境涉及数据库、Redis、Quartz、RabbitMQ、RocketMQ 等配置；未实际使用的中间件不要因为配置存在就默认启用业务能力。

## 背景与约束

当前夸友后端尚未改造，仍是上游开源基线。构建和启动问题应先按上游基线排查，再判断是否是夸友改造引入。

根 `pom.xml` 当前只启用少量核心模块，很多业务模块目录存在但未参与构建。启动失败时，不要先去修未启用模块。

## 标准做法

启动或排查本地环境前检查：

| 项 | 检查点 |
| --- | --- |
| JDK | 使用 Java 17 |
| Maven 模块 | 根 `pom.xml` 的 `<module>` |
| 启动类 | `YudaoServerApplication` |
| Profile | `application.yaml` 与 `application-local.yaml` / `application-dev.yaml` |
| 数据库 | URL、账号、库名、初始化 SQL |
| Redis | host、port、db、password |
| Quartz | 是否自动启动、表是否初始化 |
| MQ | Redis/RabbitMQ/RocketMQ 是否真的用于当前功能 |

## 禁止或谨慎做法

- 禁止把真实敏感密钥写入知识库或 docs。
- 禁止看到配置项就认为对应能力已完成夸友业务接入。
- 禁止修改 `base-package` 后不同步包名、启动扫描和 MyBatis 配置。
- 谨慎开启所有定时任务和 MQ 消费者，尤其在本地环境。
- 谨慎升级 Spring Boot、JDK、MyBatis Plus 等核心版本，必须先评估上游兼容性。

## 关键入口与定位方式

| 对象 | 路径/名称 | 用途 |
| --- | --- | --- |
| 根构建 | `ruoyi-vue-pro/pom.xml` | 模块、Java、Spring Boot 版本 |
| 启动类 | `YudaoServerApplication` | 后端启动入口 |
| 全局配置 | `application.yaml` | base-package、MyBatis、通用配置 |
| 本地配置 | `application-local.yaml` | 本地端口、中间件、数据源 |
| 开发配置 | `application-dev.yaml` | dev 环境配置 |
| 接入记录 | `docs/06-tech/02-上游源码版本记录.md` | 基线分支和 commit |

## 变更影响与检查清单

- [ ] 修改依赖版本前，确认所有启用模块可编译。
- [ ] 修改模块启用前，确认 `yudao-server` 依赖和 SQL 脚本。
- [ ] 修改 profile 前，确认本地、dev、生产的差异。
- [ ] 修改 `base-package` 前，确认扫描路径和 MyBatis 配置。
- [ ] 启动失败时先看当前启用模块，不要被未启用目录干扰。
- [ ] 知识文档中不要记录真实密钥、密码、Token、证书。

## 常见问题与踩坑

- 接口 404：可能是模块未启用、包名不被扫描、Controller 路径不匹配。
- Job 表缺失：Quartz 使用 JDBC 存储时需要对应表结构。
- Redis/MQ 配置存在但功能不可用：可能只是上游默认配置，需核对模块和业务链路是否启用。
- 敏感配置泄露：配置文件如含示例密钥，知识库只记录路径和风险，不记录值。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友本地开发 profile 标准 | 待确认 | 影响后续启动文档 |
| 是否建立 `.env` 或外部密钥管理方式 | 待确认 | 影响敏感配置安全 |
| 后端构建命令是否固定为根工程全量构建 | 待确认 | 影响开发效率和 CI |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |