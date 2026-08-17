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
- yudao-ui-admin-vue3:RULE-README
---

# yudao-ui-admin-vue3 规则知识索引

`domain/rule/` 用于沉淀管理后台权限、展示、审核、操作约束等规则。

## 当前状态

当前暂无正式 rule 知识。后台规则需等待夸友管理后台业务改造明确后再沉淀。

## 使用规则

1. 未经确认的后台权限、审核或展示规则不得写入正式 rule。
2. 需要判断后端 admin/app 权限边界时，优先读取 `../../../ruoyi-vue-pro/domain/rule/` 对应知识；如路径不适用，应回到 `applications/ruoyi-vue-pro/INDEX.md`。
3. 需要新增规则知识时，使用 `knowledge/template/rule-template.md`。
