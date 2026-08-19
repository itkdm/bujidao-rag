# docs/changes — 动态研发文档体系

本目录用于记录**一次具体研发变更**从讨论、实施到归档的完整生命周期。
它针对「事情怎么变」，而非「系统长期应该长什么样」。

---

## 1. 与 `knowledge/` 的边界

- `knowledge/`：按「是否值得**长期、跨需求复用**」组织。内容是稳定的规范、技术约束、参考资料，不随单次变更失效。
- `docs/changes/`：按「一次**具体研发变更的生命周期**」组织。内容随该变更推进、实现或被替代而流转、归档。

> 经验法则：`knowledge/` 回答「以后怎么做」；`docs/changes/` 回答「这次为什么、改成什么、怎么落」。

若某次变更沉淀出可长期复用的结论，待变更 `implemented` 且经验稳定后，再将其提炼进 `knowledge/`，并避免在两边重复维护同一信息。

---

## 2. 哪些修改需要创建 Change

满足以下任一条件，建议创建 Change：

- 非简单变更：涉及多文件、跨模块、或存在多种可行方案需要决策。
- 引入/调整架构、模块边界、技术选型。
- 影响外部契约（API、数据模型、配置、行为语义）。
- 需要记录取舍与验收依据，供后续回溯。
- 简化/重构既有结构，且存在被质疑或回退的可能。

---

## 3. 哪些简单修改通常不需要

以下通常**不需要** Change（直接在提交中说明即可）：

- 单一文件的拼写、格式、注释修正。
- 不改变行为的局部变量重命名。
- 与既有 Spec/Design 完全一致的常规 CRUD 接口实现。
- 明确属于「按既定设计填空」的增量开发。
- 依赖库小版本升级且行为无变化。

判断不清时，倾向创建轻量 Change（仅 `change.md`）。

---

## 4. 六种 Change 类型

| 类型 | 含义 |
|------|------|
| `feature` | 新增功能或能力 |
| `bug-fix` | 修复缺陷（当修复涉及设计取舍或影响面较广时） |
| `architecture` | 架构、模块边界、技术选型调整 |
| `simplification` | 简化、重构、去除冗余 |
| `process` | 研发流程、规范、工具链调整 |
| `testing` | 测试策略、覆盖率、测试基础设施变更 |

---

## 5. 四种生命周期状态

| 状态 | 含义 | 所在目录 |
|------|------|----------|
| `proposed` | 讨论中、准备实施或正在实施 | `proposed/` |
| `implemented` | 已实际实现并验证 | `implemented/` |
| `rejected` | 讨论过但最终未采用 | `rejected/` |
| `archived` | 曾经实现，但已失效或被新方案替代 | `archived/` |

流转路径：

```text
proposed → implemented → archived
proposed → rejected
```

---

## 6. 目录与命名规范

```text
docs/changes/
├── README.md
├── proposed/      # 按类型再分子目录，子目录在实际产生 Change 时创建
├── implemented/
├── rejected/
├── archived/
└── templates/     # 模板，非实际 Change
```

实际 Change 推荐路径：

```text
docs/changes/proposed/<type>/<date>-<slug>/
├── change.md          # 核心文件，必须存在
├── spec.md            # 按需
├── research.md        # 按需
├── design.md          # 按需
└── plan.md            # 按需
```

- `<type>`：见第 4 节六种类型之一。
- `<date>`：创建日期，格式 `YYYY-MM-DD`。
- `<slug>`：短横线分隔的小写英文短语，描述变更主题，如 `add-cache-layer`。

只有 `change.md` 是核心文件，其余（Spec / Research / Design / Plan）全部按需创建。
不需要为保留目录而批量制造 `.gitkeep`。

---

## 7. 五种文档各自职责

| 文档 | 职责 | 不写什么 |
|------|------|----------|
| `change.md` | 一次变更的主记录：为什么变、总体变什么、关键取舍、验收、最终决策 | 冗长的技术调研过程 |
| `spec.md` | 系统必须表现出的行为，以及如何验证行为正确 | 代码结构、具体实现设计、实施任务 |
| `research.md` | 解决影响设计的重要技术未知，为 Design 提供可靠输入 | 最终技术设计本身 |
| `design.md` | 为满足 Change/Spec 最终采用的技术方案 | 复制 Spec、任务清单、未收敛的调研过程 |
| `plan.md` | 把已确定的设计转成有顺序、有依赖、有验证方式的实施路径（兼 Task Breakdown） | — |

> Change 是中心；Spec / Research / Design / Plan 都是**按需附件**，不是固定流水线。
> 简单变更可能只有 `change.md` 即可。

---

## 8. Supplemental Documents 的创建条件

当某个 Change 复杂到单篇文档难以承载时，按需拆出专项文档（即 Supplemental Documents）：

- 行为复杂、需独立描述验收 → `spec.md`
- 存在重要技术未知、影响设计 → `research.md`
- 技术方案庞大、需独立说明 → `design.md`
- 实施路径长、需分阶段跟踪 → `plan.md`

这些文档跟随所属 Change 目录一起在生命周期中流转，**不建立独立生命周期**。
本阶段不创建独立的 `tasks.md`；仅当未来出现超大型任务、多 Agent 并行或独立状态跟踪需求时再考虑拆出。

---

## 9. 禁止重复维护同一信息

- 同一事实只应在**最合适的一篇文档**中作为权威来源。
- 其他文档引用它，而不是复制它。例如：`design.md` 引用 `spec.md` 的需求编号，而非重写需求。
- 状态流转（proposed → implemented 等）时，更新文档语义（如 Proposal → Decision），而非在多处追加历史说明。

---

## 10. Change 完成 / 拒绝 / 归档的处理

- **实现完成**：将目录从 `proposed/` 移至 `implemented/`；`change.md` 语义从「计划」转为「实际决策」
  （Proposal → Decision，Acceptance → Verification，Risks → Consequences）。
- **拒绝**：移至 `rejected/`；保留原方案并记录 Rejection 原因。
- **归档**：移至 `archived/`；记录为何归档、被哪个新 Change 替代（若存在）。

所有移动为显式操作，由用户或 Coding Agent 决定，无自动触发机制。
