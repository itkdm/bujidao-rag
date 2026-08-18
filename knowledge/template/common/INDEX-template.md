---
# 知识库 INDEX 全局通用模板
# 本文件只定义 INDEX 的通用正文结构，不承载任何具体业务、技术栈或当前文件。
id: KB-INFRA-COMMON-INDEX-TEMPLATE
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- infrastructure
- template
- index
anchors:
- GLOBAL:INDEX-TEMPLATE
---

# {目录名称}索引

> 本文件是某个 Knowledge 受管理目录的 `INDEX.md`。
> 职责边界一句话：**INDEX = 这个目录现在有什么**（动态内容索引）。
> 不要在此写目录定位、路由规则、使用规范、知识摘要或读取顺序。

## 内容索引

| 名称 | 类型 | 说明 |
|------|------|------|
| [`README.md`](./README.md) | 文件 | 当前目录的职责与维护规则 |
| [`xxx/`](./xxx/INDEX.md) | 目录 | 一句话说明该目录的作用 |
| [`xxx.md`](./xxx.md) | 文件 | 一句话说明该文件的作用 |

填写与排序规则：

1. 必须覆盖当前目录的**所有有效直接子文件和直接子目录**，只索引一层，禁止递归展开孙级内容。
2. 当前目录若存在 `README.md`，必须显式列入首行，固定为 `| [`README.md`](./README.md) | 文件 | 当前目录的职责与维护规则 |`。
3. `INDEX.md` 自身不得列入内容索引。
4. 排序固定：先 `README.md`，再按名称字典序升序列出**直接子目录**，最后按名称字典序升序列出**其他直接子文件**。
5. 子目录项统一链接到其 `INDEX.md`：`[xxx/](./xxx/INDEX.md)`，前提是该目录属于 Knowledge 受管理目录且存在 INDEX。
6. `说明` 字段只写**用途 / 职责**（purpose），不写动态内容摘要（content summary）。例如「记录应用当前已确认的功能能力与主要业务流程」，而不是「当前包含登录、用户、支付等功能」。

## 补充说明

可选。

仅记录无法通过内容索引表达、但理解当前索引确实必要的信息。

没有内容时整个章节省略。

---

## 使用约束（模板说明，不写入实际 INDEX）

- INDEX 不得包含：目录定位、路由规则、使用规范、知识摘要、读取顺序等章节。
- INDEX 不得索引自身，不得递归索引孙级内容。
- INDEX 不得把「详细任务路由 / 深层文件清单 / 动态知识摘要」写入正文；这些由 `ROUTING.md` 或子目录 INDEX 承担。
