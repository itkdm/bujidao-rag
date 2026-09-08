
# API 入口索引

## AI 使用摘要

- 适用场景：查找 Controller、接口前缀、模块间 API、接口文档入口时
- 关键入口：`yudao-module-system/src/main/java/.../controller/`
- 关键事实：当前 system 模块同时存在 `controller.admin` 和 `controller.app`；模块间 API 位于 `api/`；Controller 通常返回 `CommonResult`
- 关联知识：[tech-framework-web-api.md](../tech/tech-framework-web-api.md)、[base-permission-index.md](./base-permission-index.md)
- 使用前必须核对：接口端类型、Controller 路径、权限注解、OpenAPI 注解

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | [`ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/`](../../../../ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/) | 当前 Controller 入口 |
| code | [`ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/api/`](../../../../ruoyi-vue-pro/yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/api/) | 当前模块间 API 入口 |
| code | [`ruoyi-vue-pro/yudao-server/src/main/resources/application.yaml`](../../../../ruoyi-vue-pro/yudao-server/src/main/resources/application.yaml) | 全局 API 相关配置入口 |
| doc | [`knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/07.接口文档.md`](<../../../reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/07.接口文档.md>) | 官方接口文档说明 |
| doc | [`knowledge/reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md`](<../../../reference/ruoyi-vue-pro官方文档/01.开发指南/01.萌新必读/09.项目结构.md>) | 官方 admin/app Controller 分层说明 |

## 索引范围

本文索引后端 API 的代码入口、端侧分类、典型 Controller、模块间 API 路径和接口文档入口。

## 不收录范围

本文不解释 Controller 编写规范；相关实现约束见 [`tech-framework-web-api.md`](../tech/tech-framework-web-api.md)。

## 事实索引

| 对象 | 路径/名称 | 类型 | 说明 |
| --- | --- | --- | --- |
| 管理后台 Controller | `yudao-module-system/.../controller/admin/` | Java package | 管理后台接口入口 |
| 用户端 Controller | `yudao-module-system/.../controller/app/` | Java package | app/小程序接口入口 |
| 模块间 API | `yudao-module-system/.../api/` | Java package | 暴露给其他模块的 API 接口和实现 |
| 字典 Controller 示例 | `controller/admin/dict/DictTypeController.java` | Controller | CRUD、权限、分页、导出示例 |
| app 字典 Controller | `controller/app/dict/AppDictDataController.java` | Controller | app 端接口示例 |
| 权限 Controller | `controller/admin/permission/` | Controller package | 菜单、角色、权限分配接口 |
| 认证 Controller | `controller/admin/auth/AuthController.java` | Controller | 管理后台登录认证入口 |

## 命名与定位规则

- 管理后台接口类通常位于 `controller.admin.{biz}`。
- App 端接口类通常位于 `controller.app.{module}`，类名常带 `App` 前缀。
- Controller 入参/出参 VO 通常放在同级 `vo` 包下。
- 模块间调用接口位于 `api/{biz}`，实现类通常命名为 `{Name}ApiImpl`。

## 关键路径

| 路径 | 用途 | 备注 |
| --- | --- | --- |
| `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/admin/` | 管理后台 API | 当前 Controller 最密集的入口 |
| `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/controller/app/` | app API | 当前已有字典、地区、租户等接口 |
| `yudao-module-system/src/main/java/cn/iocoder/yudao/module/system/api/` | 模块间 API | 权限、用户、短信、通知等能力 |
| `knowledge/reference/ruoyi-vue-pro官方文档/.../07.接口文档.md` | 官方接口文档说明 | 查接口文档使用方式 |

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `tech/` | API 返回、校验和 Controller 约束见 [`tech-framework-web-api.md`](../tech/tech-framework-web-api.md) |
| `feature/` | 后续具体功能流程会引用对应 Controller |
| `rule/` | 权限、展示、状态等规则会影响 API 行为 |

## 变更影响

Controller 路径、API 前缀、VO 名称变化会影响前端调用、小程序联调、接口文档、权限菜单和 AI 代码定位。

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 3 | 2026-08-23 | 移除具体业务耦合并校准为通用芋道示例 | Codex |
| 4 | 2026-08-24 | 将目标项目初始化决策移至初始化 Skill 清单 | Codex |
