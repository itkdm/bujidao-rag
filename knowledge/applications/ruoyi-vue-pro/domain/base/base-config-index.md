---
# ==================== 必填字段 ====================
id: KB-BASE-KUAYOU-RUOYI-VUE-PRO-CONFIG
type: base
scope: ruoyi-vue-pro
# 业务归属
domain: kuayou
application: ruoyi-vue-pro
appType: 后端应用

# 基础索引分类
baseArea: config
topic: config-index

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
    ref: ruoyi-vue-pro/yudao-server/src/main/resources/application.yaml
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-server/src/main/resources/application-local.yaml
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/yudao-server/src/main/resources/application-dev.yaml
    verifiedAt: 2026-08-09
  - type: code
    ref: ruoyi-vue-pro/pom.xml
    verifiedAt: 2026-08-09
  - type: doc
    ref: knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/05.快速启动【后端】.md

# 标签与锚点
tags:
  - backend
  - config
  - profile
  - yaml
anchors:
  - APPLICATION:ruoyi-vue-pro
  - BASE_AREA:config
  - BASE_TOPIC:config-index
---

# 配置入口索引

## AI 使用摘要

- 适用场景：定位后端 profile、端口、数据源、Redis、Quartz、MQ、base-package 配置时
- 关键入口：`yudao-server/src/main/resources/application*.yaml`
- 关键事实：本地/开发端口配置在 profile 文件；`yudao.info.base-package` 影响扫描范围；配置文件可能包含示例密钥但知识库不记录真实值
- 关联知识：[tech-build-env-local.md](../../tech/tech-build-env-local.md)
- 使用前必须核对：当前运行 profile、敏感配置是否外部化、目标中间件是否实际启用

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | `application.yaml` | 全局默认配置 |
| code | `application-local.yaml` | 本地环境配置 |
| code | `application-dev.yaml` | dev 环境配置 |
| code | `pom.xml` | Java、Spring Boot、Maven 配置入口 |
| doc | `05.快速启动【后端】.md` | 官方后端启动说明 |

## 索引范围

本文索引后端配置文件、profile、关键配置项位置和中间件配置入口。

## 不收录范围

本文不记录真实密码、密钥、Token、证书等敏感值；也不解释配置取舍，配置约束见 `tech/`。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| 全局配置 | `yudao-server/src/main/resources/application.yaml` | YAML | 默认配置、base-package、MyBatis、WebSocket 等 |
| 本地配置 | `yudao-server/src/main/resources/application-local.yaml` | YAML | local 环境端口、数据源、Redis、Quartz、MQ |
| 开发配置 | `yudao-server/src/main/resources/application-dev.yaml` | YAML | dev 环境端口、数据源、Redis、Quartz、MQ |
| 日志配置 | `yudao-server/src/main/resources/logback-spring.xml` | XML | 后端日志配置 |
| 根构建配置 | `ruoyi-vue-pro/pom.xml` | Maven | Java 17、Spring Boot 版本、模块启用 |
| base package | `yudao.info.base-package` | YAML property | 影响 Spring 扫描和 MyBatis 类型别名 |
| 服务端口 | `server.port` | YAML property | local/dev 当前配置入口 |

## 命名与定位规则

- 全局配置文件为 `application.yaml`。
- 环境配置使用 `application-{profile}.yaml`。
- 本地开发通常看 `application-local.yaml`。
- 不同中间件配置可能分散在多个 `spring:` 块或独立配置块中。
- 敏感值只记录配置项路径，不复制具体值。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `yudao-server/src/main/resources/application.yaml` | 全局默认配置 | 查 base-package、MyBatis、WebSocket |
| `yudao-server/src/main/resources/application-local.yaml` | 本地运行配置 | 查本地数据源、Redis、Quartz |
| `yudao-server/src/main/resources/application-dev.yaml` | dev 环境配置 | 查 dev 数据源和中间件 |
| `ruoyi-vue-pro/pom.xml` | 构建配置 | 查 Java 17、Spring Boot 3.5.15 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | 本地构建与环境约束见 `tech-build-env-local.md` |
| `domain/feature/` | 功能启用后可能需要新增配置项 |
| `domain/rule/` | 安全、权限、租户规则可能影响配置 |

## 变更影响

配置文件变化会影响启动、接口前缀、数据库连接、Redis、Quartz、MQ、WebSocket、AI 后续排障路径。

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 夸友本地 profile 是否固定使用 `local` | 待确认 | 影响启动和排障文档 |
| 敏感配置是否迁移到外部环境变量 | 待确认 | 影响配置安全 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |