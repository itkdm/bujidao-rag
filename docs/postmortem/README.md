# Postmortem — 事后分析

本目录存放 **Postmortem（事后分析）**：针对已经发生、并且逃过了现有防线的问题做事后分析。

本目录只提供通用事后分析结构，不预置任何行业、产品或功能模块的事故样例；实际文件必须来自目标项目已经发生的真实问题。

本文件是 Postmortem 定义、触发条件、文件位置和内容边界的唯一权威来源。Change 与 Postmortem 的关系见 [Change 规范](../changes/README.md) 第 11 节。

---

## 定位

Postmortem 解释：

> **为什么这个问题能够发生并逃过现有防线，以及以后如何让同类问题更早、更响亮地失败。**

它不负责「怎么修 Bug」（那是 bug-fix Change）、「准备采用什么新方案」（Change / Design）、「具体开发步骤」（Plan）。

## 触发条件（比 Change 更克制）

采用「两条 AND」的克制规则，避免「三选一」过宽：

```text
通常应至少满足：
1. 问题具有明显隐蔽性，或高重新发现成本
   AND
2. 暴露出现有测试 / Review / CI / 工具 / 流程的系统性防线缺口
```

- 第 1 条保证「值得写」；仅「调试了三小时但根因普通」不算。
- 第 2 条保证「防线没工作」，而非单纯个人失误。

**直接创建（豁免上述两条）**：生产事故、安全问题、严重数据一致性问题、重大发布故障。

**不写**：普通 NullPointerException（忘记判空）、变量写错、普通字段错误、简单兼容问题、测试已正常失败并阻止合并——这些说明工程防线已正常工作；仅满足单条（如只调试久但根因普通、或仅普通 Bug 但防线本正常工作）的，也优先用 bug-fix Change 而非 Postmortem。

## 命名

沿用 Change 的 `日期 + slug` 风格：

```text
docs/postmortem/
├── README.md
├── 2026-08-23-wrong-session-validation.md
└── 2026-08-24-lock-failure-in-multi-instance.md
```

无生命周期目录（Postmortem 是已发生的事实，不流转 proposed/implemented/archived）。

## 内容边界

| 章节 | 必选 | 说明 |
|------|------|------|
| `## 执行摘要` | 必选 | Executive Summary：一句话结论 + 影响 |
| `## 影响与发生了什么` | 必选 | Impact / What Happened：发生了什么、影响范围 |
| `## 时间线（推荐，可简化）` | 推荐（可简化） | Timeline：大型事故记精确时间线；普通 Bug 简化为 发现→误判→排查→根因→修复 |
| `## 根因` | **必选** | Root Cause：真正根因 |
| `## 为什么逃过防线` | **必选** | Why It Escaped：分测试、评审、工具 / CI、流程 / 规范四线说明防线为何没工作 |
| `## 防线（Guardrails）` | **必选** | 具体落地防线：测试、CI、规范、工具，并链接对应 Change |
| `## 关联变更` | 可选 | Related Changes：关联的 Change 路径（Postmortem 通常催生新 Change） |

表内代码格式是实例必须使用的精确二级标题，所有必选章节都必须包含实际内容。`## 为什么逃过防线` 下还必须使用并填写四个精确三级标题：`### 测试`、`### 评审`、`### 工具 / CI`、`### 流程 / 规范`。

最重要三块是：**根因 + 为什么逃过防线 + 防线**。
> 模板见 [`templates/postmortem.md`](./templates/postmortem.md)。
