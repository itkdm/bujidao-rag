---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-CANDIDATE-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 3
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- global
anchors:
- GLOBAL:CANDIDATE-README
---

# candidate/

## 目录定位

`candidate/` 用于存放 AI 推断、新发现、待确认规则和暂未进入正式知识库的线索，是正式知识入库前的暂存与确认区。

## 应包含的内容

- AI 分析出的推断结论、新发现与待确认规则。
- 暂未进入正式知识库、需要标注意愿来源和可信度的线索。
- 写明来源、证据、可信度和待确认问题的候选知识文件。

## 不应包含的内容

- 已经 owner review 确认的正式知识：应迁移到 `main/` 或 `applications/` 的合适位置。
- 个人经验或碎片素材：应放入 `personal/`，确认后再进入本目录或正式目录。
- 已证明不适用的内容：应标记为废弃或迁移到 `archive/`，不继续作为 AI 读取入口。

## 维护规则

- 只要结论没有经过 owner 确认，先放入 `candidate/`，不要直接写入 `main/` 或 `applications/`。
- 候选知识必须写明来源、证据、可信度和待确认问题。
- 候选知识被确认后，再迁移到 `main/` 或 `applications/` 的合适位置。
- 被证明不适用的候选知识，应标记为废弃或迁移到归档，不继续作为 AI 读取入口。
