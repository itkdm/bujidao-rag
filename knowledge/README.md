---
# 知识库基础设施文件
id: KB-INFRA-README
scope: cross-app
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-17
verifiedAt: 2026-08-17
tags:
- global
- overview
anchors:
- GLOBAL:README
---

# 知识库定位

本知识库是 AI 研发交付底座的**知识资产层**，负责沉淀团队的稳定上下文，为 Coding Agents 提供准确、可路由、可验证的知识来源。

## 核心原则

### 原则 1：分层设计，各司其职

| 目录/文件 | 职责 | 详细内容 |
|-----------|------|----------|
| `main/` | 跨应用、跨系统、跨业务线的**通用知识** | 核心术语、跨应用流程、通用状态定义、全局技术约束、多应用都要遵守的业务规则 |
| `applications/` | 应用范围内的知识 | 应用总览、tech（应用级技术约束）等 |
| `candidate/` | 候选知识暂存区 | AI 分析出的推断结论先放这里，标注意愿来源和可信度，经 owner review 后才转正式 |
| `personal/` | 个人研发经验和踩坑记录 | 个人工作区，验证后可转为 candidate 再进正式知识库 |
| `template/` | 强约束的知识写作模板 | 固定知识的结构、状态、证据来源，防止 AI 写作粒度漂移 |
| `archive/` | 已废弃或过期知识的归档区 | 不再作为正式引用来源，仅用于历史追溯 |

### 原则 2：KB 提供稳定上下文，当前代码仍然是实现事实

> 尤其是接口签名、DTO 字段、Topic 配置、feature key、状态枚举、开关配置这类容易变化的内容，知识库**只提供定位入口**。真正改代码前，必须回到当前仓库核对真实代码。

### 原则 3：渐进式加载，不全量读取

复杂业务里的上下文不是塞得越多越好。AI 应通过 `ROUTING.md` 先定位，再按需求关键词、业务身份、状态码、接口名等线索，**逐步加载正确粒度的上下文**。

### 原则 4：两个入口，两种场景

| 场景 | 入口文件 | 说明 |
|------|----------|------|
| 会话级初始化 | `KNOWLEDGE-RULES.md` | 首次接触知识库时读取，理解全局规则 |
| 需求级检索 | `ROUTING.md` | 每个具体需求开始时读取，定位目标知识 |

---

## 目录结构

```text
knowledge/
  KNOWLEDGE-RULES.md   # 全局规则（基础设施）
  ROUTING.md           # 知识检索路由表（基础设施）
  README.md            # 知识库定位说明（基础设施）
  INDEX.md             # 全局索引（基础设施）
  template/            # 写作模板（基础设施）
  main/                # 全局层：跨应用的知识
  applications/        # 应用层：应用或模块内的知识
  reference/           # 参考源层：上游官方文档、外部文章、证据材料
  candidate/           # 候选层：待 owner review 的 AI 推断与新发现
  personal/            # 个人层：踩坑记录、碎片笔记、原始经验
  archive/             # 归档层：已废弃或过期知识
```

---

## 知识流转路径

```
personal/ 个人经验
    ↓ （验证后）
candidate/ 候选知识（DRAFT → CANDIDATE）
    ↓ （owner review）
main/ 或 applications/ 正式知识（OFFICIAL）
    ↓ （代码/业务变化）
DEPRECATED（原地标记，保留历史）
```

- **禁止** AI 直接将未确认内容写入 `main/` 或 `applications/` 正式目录
- **禁止** AI 将个人经验直接当作团队结论引用

---

## AI 使用指引

> 当 AI 需要使用本知识库时，请遵守以下顺序：
>
> **首次接触知识库**：
> 1. 读取 `KNOWLEDGE-RULES.md` → 理解全局规则
>
> **每个具体需求**：
> 1. 读取 `ROUTING.md` → 根据需求关键词定位到候选业务域和应用
> 2. 按路由结果进入 `main/` 或 `applications/` 下的具体文件
> 3. **最后必须回到当前应用仓库核对代码**
>
> **如需了解知识库整体结构和原则**：
> - 读取本文件（`README.md`）