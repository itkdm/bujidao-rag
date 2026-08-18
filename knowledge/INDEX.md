---
# 知识库基础设施文件
id: KB-INFRA-GLOBAL-INDEX
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 2
updatedAt: 2026-08-18
verifiedAt: 2026-08-17
tags:
- global
- index
anchors:
- GLOBAL:INDEX
---

# 全局索引

这是知识库的全局索引。

AI 在读取 `ROUTING.md` 后，应通过本文档定位相关知识域、应用、模块和主题。

## 全局层

- `main/`：跨应用共享的业务概念、术语、通用流程和全局约束。
  - `main/rules/`：全局协作规范（Git Commit、分支规范、Code Review 等）
  - `main/tech/`：跨应用共享的技术知识和技术约束

## 应用层

- `applications/`：按应用或模块组织的知识。此目录在项目初始化时根据实际业务需求生成，公共知识库不预设具体应用。
  - 示例：`applications/{appCode}/`：某应用的开源基线及目标知识。

## 参考源层

- `reference/`：上游官方文档、外部文章、开源项目说明等证据材料。这里不是正式知识入口，AI 仅在需要核对证据时读取。
  - 示例：`reference/{upstreamName}/`：某上游项目的官方文档抓取副本。

## 输入层

- `candidate/`：AI 推断和新发现，等待 owner review。目录结构镜像正式目录。
- `personal/`：个人笔记、踩坑记录和原始经验素材。

## 模板层

- `template/`：知识写作模板和结构约束。
  - `template/application-template.md`：应用级知识模板。
  - `template/base-template.md`：基础事实索引模板。
  - `template/base-index-template.md`：应用内 `domain/base/` 索引模板。
  - `template/rule-template.md`：规则知识模板。
  - `template/rule-index-template.md`：应用内 `domain/rule/` 索引模板。
  - `template/tech-template.md`：技术知识模板。
  - `template/tech-index-template.md`：应用内 `tech/` 索引模板。

## 归档层

- `archive/`：已废弃、过期或不再维护的知识归档。归档知识不再作为正式引用来源，仅用于历史追溯。