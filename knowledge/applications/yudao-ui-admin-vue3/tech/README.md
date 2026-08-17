---
# 知识库导航基础设施文件
id: KB-NAV-yudao-ui-admin-vue3-README
scope: app-specific
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-17
verifiedAt: 2026-08-17
tags:
- navigation
- yudao-ui-admin-vue3
anchors:
- yudao-ui-admin-vue3:TECH-README
---

# yudao-ui-admin-vue3 技术知识索引

本文档是 `yudao-ui-admin-vue3` 的 `tech/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体技术知识。

## 使用规则

1. 修改管理后台代码前，先判断任务属于哪个技术分类。
2. 只读取与当前任务相关的技术文档，避免全量加载。
3. 没有正式知识时，先查 `candidate/`，仍无法确认时回到代码事实。
4. 新增技术知识必须使用 `knowledge/template/tech-template.md`。

## 技术分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| architecture | 前端架构约束、页面/模块边界、后台能力拆分 | `tech-architecture-{topic}.md` |
| framework | Vue3、Element Plus、Vite、Pinia、路由、目录约定 | `tech-framework-{topic}.md` |
| api-integration | Axios、API 封装、接口错误处理、后端联调约束 | `tech-api-{topic}.md` |
| data-transaction | 前端缓存、状态管理、表单状态、一致性展示 | `tech-data-{topic}.md` |
| async-job | 异步请求、轮询、WebSocket、后台任务前端展示 | `tech-async-{topic}.md` |
| error-observability | 前端异常、日志、埋点、提示、排障入口 | `tech-error-{topic}.md` |
| security-permission | 登录态、路由权限、按钮权限、数据可见性 | `tech-security-{topic}.md` |
| build-env | pnpm、Vite、环境变量、构建发布、本地启动 | `tech-build-{topic}.md` |
| testing-quality | 组件测试、类型检查、Lint、代码质量 | `tech-test-{topic}.md` |
| troubleshooting | 管理后台常见问题、构建失败、接口联调问题排查 | `tech-troubleshooting-{topic}.md` |

## 当前技术知识

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 暂无 | - | - | 后续按实际管理后台改造逐步补充 |
