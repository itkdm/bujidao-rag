# {appCode} 规则知识索引

本文档是 `{appCode}` 的 `domain/rule/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体规则知识。

## 使用规则

1. `rule/` 只记录稳定规则和约束，不记录事实入口，也不展开实现方案。
2. 需要定位对象在哪，转到 `domain/base/`。
3. 需要了解怎么实现，转到 `tech/`。
4. 需要了解完整业务流程，转到 `domain/feature/`。
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
| 暂无 | - | - | 后续按稳定规则逐步补充 |
