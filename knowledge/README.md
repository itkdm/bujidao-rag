---
# 知识库基础设施文件
id: KB-INFRA-GLOBAL-README
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- global
- overview
anchors:
- GLOBAL:README
---

# 知识库

## 目录定位

本知识库是 AI 研发交付底座的**知识资产层**，负责沉淀团队的稳定上下文，为 Coding Agents 提供准确、可路由、可验证的知识来源。

整个知识库按分层设计组织，各层目录各司其职：

- `main/`：跨应用、跨系统、跨业务线的通用知识（核心术语、跨应用流程、通用状态定义、全局技术约束、多应用都要遵守的业务规则）。
- `applications/`：应用或模块范围内的知识（应用总览、功能、规则、技术约束、基础事实等）。
- `candidate/`：候选知识暂存区，AI 分析出的推断结论先放这里，经 owner review 后才转正式。
- `personal/`：个人研发经验和踩坑记录，验证后可转为 candidate 再进正式知识库。
- `template/`：强约束的知识写作模板与导航模板基础设施。
- `reference/`：上游官方文档、外部文章、开源项目说明等证据材料（本次不强制纳入双文件协议）。

知识库提供稳定上下文；当前代码仍然是实现事实。尤其接口签名、DTO 字段、Topic 配置、feature key、状态枚举、开关配置等易变内容，知识库只提供定位入口，真正改代码前必须回到当前仓库核对真实代码。

## 应包含的内容

- 各层目录的稳定职责说明与维护契约。
- 跨应用 / 应用内 / 候选 / 个人的结构化知识文件（feature、rule、tech、base、flow、state、glossary 等类型）。
- 基础设施文件：`README.md`、`INDEX.md`、`ROUTING.md`、`KNOWLEDGE-METADATA-RULES.md`、`template/`、辅助脚本。

## 不应包含的内容

- 动态文件清单与内容索引：应放在各目录的 `INDEX.md`。
- 用户具体任务路由与 Agent 读取链：应放在 `ROUTING.md`。
- 全局 Metadata 字段规范：应放在 `KNOWLEDGE-METADATA-RULES.md`。
- 真实代码实现、未确认的业务推断：推断先入 `candidate/`，不要直接写入正式目录。

## 维护规则

- AI 应通过 `ROUTING.md` 先定位，再按需求关键词、业务身份、状态码、接口名等线索逐步加载正确粒度的上下文，不全量读取。
- 禁止 AI 直接将未确认内容写入 `main/` 或 `applications/`；禁止将个人经验直接当作团队结论引用。
- 知识流转：`personal/` → `candidate/` →（owner review）→ `main/` 或 `applications/`；代码 / 业务变化后原地标记 `DEPRECATED` 保留历史。
- 所有受管理 Markdown 文件必须遵守 `KNOWLEDGE-METADATA-RULES.md`，并通过 `scripts/validate_metadata.py` 校验。

## 补充说明

`archive/` 用于归档已废弃或过期知识，不再作为正式引用来源，仅用于历史追溯（本次未纳入受管理目录双文件协议范围）。
