---
# 知识库导航基础设施文件
id: KB-NAV-yudao-mall-uniapp-README
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
- yudao-mall-uniapp
anchors:
- yudao-mall-uniapp:TECH-README
---

# yudao-mall-uniapp 技术知识索引

本文档是 `yudao-mall-uniapp` 的 `tech/` 入口。AI 或开发者进入本目录时，应先读本文件，再按任务类型选择具体技术知识。

## 使用规则

1. 修改学生端/小程序代码前，先判断任务属于哪个技术分类。
2. 只读取与当前任务相关的技术文档，避免全量加载。
3. 没有正式知识时，先查 `candidate/`，仍无法确认时回到代码事实。
4. 新增技术知识必须使用 `knowledge/template/tech-template.md`。

## 技术分类路由

| 分类 | 适用问题 | 推荐文件命名 |
| --- | --- | --- |
| architecture | 端侧架构约束、页面/分包边界、商城模板改造边界 | `tech-architecture-{topic}.md` |
| framework | uni-app、Vue3、Pinia、路由、页面生命周期、目录约定 | `tech-framework-{topic}.md` |
| api-integration | 请求封装、接口错误处理、登录态、后端联调约束 | `tech-api-{topic}.md` |
| data-transaction | 本地缓存、购物车状态、表单状态、端侧一致性 | `tech-data-{topic}.md` |
| async-job | 异步请求、轮询、订阅消息、端侧任务状态展示 | `tech-async-{topic}.md` |
| error-observability | 小程序异常、日志、用户提示、排障入口 | `tech-error-{topic}.md` |
| security-permission | 登录鉴权、微信授权、用户信息、端侧安全边界 | `tech-security-{topic}.md` |
| build-env | HBuilderX/CLI、环境变量、微信小程序构建与发布 | `tech-build-{topic}.md` |
| testing-quality | 真机验证、兼容性检查、代码质量 | `tech-test-{topic}.md` |
| troubleshooting | 小程序常见问题、构建失败、真机异常、接口联调问题排查 | `tech-troubleshooting-{topic}.md` |

## 当前技术知识

| 主题 | 文件 | 状态 | 说明 |
| --- | --- | --- | --- |
| 暂无 | - | - | 后续按实际学生端改造逐步补充 |
