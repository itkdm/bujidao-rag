# {appCode} 基础事实索引

本文档是 `{appCode}` 的 `domain/base/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体事实索引。

## 使用规则

1. `base/` 只记录事实入口，不解释实现方案。
2. 修改代码前，如果需要定位模块、接口、模型、表、配置、权限、消息或任务，先读本文件。
3. 需要了解“怎么实现、为什么这样实现”，转到 `tech/`。
4. 需要了解业务流程，转到 `domain/feature/`。
5. 需要了解业务规则，转到 `domain/rule/`。
6. 新增基础事实索引必须使用 `knowledge/template/base-template.md`。

## 基础分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| module | 模块、包结构、启用状态、核心路径 | `base-module-{topic}.md` |
| api | Controller、API 前缀、接口入口、接口文档 | `base-api-{topic}.md` |
| model | DO、ReqVO、RespVO、DTO、Enum、ErrorCode | `base-model-{topic}.md` |
| database | SQL、表、字段、索引、逻辑删除、Quartz 表 | `base-database-{topic}.md` |
| config | YAML、profile、环境变量、中间件配置 | `base-config-{topic}.md` |
| permission | 权限编码、角色、菜单、数据权限入口 | `base-permission-{topic}.md` |
| async | MQ、Message、Producer、Consumer、Job | `base-async-{topic}.md` |

## 当前基础索引

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 暂无 | - | - | 后续按实际代码逐步补充 |
