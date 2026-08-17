---
id: KB-ENTRY-KUAYOU-RUOYI-VUE-PRO-RULE-INDEX
type: index
domain: kuayou
application: ruoyi-vue-pro
status: DRAFT
owner: bujidao
version: 2
updatedAt: 2026-08-09 15:55:00
---

# ruoyi-vue-pro 规则知识索引

本文档是 `ruoyi-vue-pro` 的 `domain/rule/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体规则知识。

## 使用规则

1. `rule/` 只记录稳定规则和约束，不记录事实入口，也不展开实现方案。
2. 需要定位对象在哪，转到 `domain/base/README.md`。
3. 需要了解怎么实现，转到 `tech/README.md`。
4. 需要了解完整业务流程，先读 `domain/feature/README.md`；当前无正式 feature 知识时，回到 `docs/01-product/` 或向布吉岛确认。
5. 未确认规则先进入 `candidate/`，不要直接进入正式 `rule/`。
6. 新增规则知识必须使用 `knowledge/template/rule-template.md`。

## 规则分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| boundary | 应用边界、模块边界、端侧边界、基线边界 | `rule-boundary-{topic}.md` |
| permission | 角色权限、接口权限、数据权限 | `rule-permission-{topic}.md` |
| status | 状态定义、状态流转、状态兼容 | `rule-status-{topic}.md` |
| data-visibility | 数据可见性、字段展示、列表范围 | `rule-data-{topic}.md` |
| security | 敏感信息、鉴权、安全例外 | `rule-security-{topic}.md` |
| config | 配置启用、环境差异、开关边界 | `rule-config-{topic}.md` |
| compliance | 合规、审计、追责要求 | `rule-compliance-{topic}.md` |

## 当前规则知识

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 后端基线边界规则 | [rule-boundary-backend-baseline.md](./rule-boundary-backend-baseline.md) | DRAFT | 防止把上游开源基线误读为夸友已改造后端 |
| 后台与用户端权限边界规则 | [rule-permission-admin-app-boundary.md](./rule-permission-admin-app-boundary.md) | DRAFT | 区分 admin/app 接口、功能权限和数据权限边界 |

## 常见任务路由

| 任务 | 优先读取 |
| --- | --- |
| 判断上游模块能否当成夸友能力使用 | `rule-boundary-backend-baseline.md` |
| 判断目录存在是否等于模块启用 | `rule-boundary-backend-baseline.md` |
| 新增管理后台接口权限 | `rule-permission-admin-app-boundary.md` |
| 判断是否可以关闭数据权限 | `rule-permission-admin-app-boundary.md` |
| 判断 app 接口是否能使用后台权限规则 | `rule-permission-admin-app-boundary.md` |
