---
# ==================== 全局必填字段 ====================
id: KB-TECH-INDEX-{APP-CODE}
type: tech
scope: app
appCode: {registered-app-code}
status: DRAFT
owner: {registered-owner}
maintainers:
  - {registered-user}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
tags:
  - {tag1}
  - {tag2}
anchors:
  - APP:{APP-CODE}
  - TECH:INDEX

# ==================== 知识字段 ====================
confidence: medium
stability: evolving
evidence:
  - type: doc
    ref: {tech 索引维护说明}
  - type: human
    ref: {确认人/时间}
---

# {appCode} 技术知识索引

本文档是 `{appCode}` 的 `tech/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体技术知识。

## 使用规则

1. 修改代码前，先判断任务属于哪个技术分类。
2. 只读取与当前任务相关的技术文档，避免全量加载。
3. 没有正式知识时，先查 `candidate/`，仍无法确认时回到代码事实。
4. 新增技术知识必须使用 `knowledge/template/tech-template.md`。

## 技术分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| architecture | 架构约束、模块边界、重要设计取舍 | `tech-architecture-{topic}.md` |
| framework | 框架用法、目录约定、生命周期、脚手架能力 | `tech-framework-{topic}.md` |
| api-integration | HTTP API、外部系统、客户端封装、接口调用约束 | `tech-api-{topic}.md` |
| data-transaction | 数据库、事务、缓存、幂等、一致性 | `tech-data-{topic}.md` |
| async-job | MQ、事件、定时任务、异步处理、WebSocket | `tech-async-{topic}.md` |
| error-observability | 异常处理、日志、监控、告警、排障入口 | `tech-error-{topic}.md` |
| security-permission | 登录鉴权、权限、租户、数据权限、安全边界 | `tech-security-{topic}.md` |
| build-env | 构建、部署、环境变量、本地启动、依赖版本 | `tech-build-{topic}.md` |
| testing-quality | 测试、代码质量、检查清单、质量门禁 | `tech-test-{topic}.md` |
| troubleshooting | 常见问题、踩坑、稳定排查路径 | `tech-troubleshooting-{topic}.md` |

## 当前技术知识

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 暂无 | - | - | 后续按实际代码改造逐步补充 |
