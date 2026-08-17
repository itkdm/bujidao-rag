---
# 知识库导航基础设施文件
id: KB-NAV-GLOBAL-README
scope: cross-app
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-17
verifiedAt: 2026-08-17
tags:
- navigation
- GLOBAL
anchors:
- GLOBAL:CANDIDATE-README
---

# 候选知识索引

`candidate/` 用于存放 AI 推断、新发现、待确认规则和暂未进入正式知识库的线索。

## 当前状态

当前暂无候选知识文件。

## 使用规则

1. 只要结论没有经过布吉岛确认，先放入 `candidate/`，不要直接写入 `main/` 或 `applications/`。
2. 候选知识必须写明来源、证据、可信度和待确认问题。
3. 候选知识被确认后，再迁移到 `main/` 或 `applications/` 的合适位置。
4. 被证明不适用的候选知识，应标记为废弃或迁移到归档，不继续作为 AI 读取入口。
