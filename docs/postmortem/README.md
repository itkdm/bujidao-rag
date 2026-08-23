# Postmortem — 事后分析

本目录存放 **Postmortem（事后分析）**：针对已经发生、并且逃过了现有防线的问题做事后分析。

> 完整定义与触发条件见 `../changes/README.md` 第 11 节。本目录只放实际 Postmortem 文件与导航。

---

## 定位

Postmortem 解释：

> **为什么这个问题能够发生并逃过现有防线，以及以后如何让同类问题更早、更响亮地失败。**

它不负责「怎么修 Bug」（那是 bug-fix Change）、「准备采用什么新方案」（Change / Design）、「具体开发步骤」（Plan）。

## 触发条件（比 Change 更克制）

默认需**同时满足**三个维度才创建：

| 维度 | 含义 |
|------|------|
| 隐蔽性 | 根因具有隐蔽性、反直觉 |
| 系统性 | 存在系统性防线缺口、架构 / 工具机制导致隐蔽故障 |
| 复现成本 | 未来重新发现成本较高（同类反复、Agent 易再犯） |

**直接创建（豁免三维度同时满足）**：严重生产事故、安全漏洞、数据一致性故障、发布流程故障。

**不写**：普通 NullPointerException（忘记判空）、变量写错、普通字段错误、简单兼容问题、测试已正常失败并阻止合并——这些说明工程防线已正常工作；仅满足三维度中个别项、但问题普通且一次修好、未来不易再犯的，也优先用 bug-fix Change 而非 Postmortem。

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
| Executive Summary | 必选 | 一句话结论 + 影响 |
| Impact / What Happened | 必选 | 发生了什么、影响范围 |
| Timeline | 推荐（可简化） | 大型事故记精确时间线；普通 Bug 简化为 发现→误判→排查→根因→修复 |
| Root Cause | **必选** | 真正根因 |
| Why It Escaped | **必选** | 分 Tests / Review / Tooling·CI / Process·Rules 四线说明防线为何没工作 |
| Guardrails | **必选** | 具体落地防线：Test / CI / Rule / Tooling，并链接对应 Change |
| Related Changes | 可选 | 关联的 Change 路径（Postmortem 通常催生新 Change） |

> 最重要三块：**Root Cause + Why It Escaped + Guardrails**。
> 模板见 `templates/postmortem.md`（本目录 `docs/postmortem/templates/`）。
