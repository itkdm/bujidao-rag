# docs/changes — 动态研发文档体系

本目录用于记录**一次具体研发变更**从讨论、实施到归档的完整生命周期。
它针对「事情怎么变」，而非「系统长期应该长什么样」。

本框架不预设任何产品、行业、功能模块或技术栈。模板仓库只提供文档结构；实际 Change 必须在目标项目中根据真实变更创建，不附带示例业务结论。

---

## 1. 与 `knowledge/` 的边界

- `knowledge/`：按「是否值得**长期、跨需求复用**」组织。内容是稳定的规范、技术约束、参考资料，不随单次变更失效。
- `docs/changes/`：按「一次**具体研发变更的生命周期**」组织。内容随该变更推进、实现或被替代而流转、归档。

> 经验法则：`knowledge/` 回答「以后怎么做」；`docs/changes/` 回答「这次为什么、改成什么、怎么落」。

若某次变更沉淀出可长期复用的结论，待变更 `implemented` 且经验稳定后，再将其提炼进 `knowledge/`，并避免在两边重复维护同一信息。

---

## 2. 哪些修改需要创建 Change

核心判断（满足任一即建议创建 Change）：

- 是否改变系统行为？
- 是否改变契约（API、数据模型、配置、行为语义）？
- 是否产生重要设计决策或取舍？
- 是否改变架构 / 模块边界 / 数据 / 配置？
- 以后是否有必要知道「为什么这样改」？

辅助信号（可作为参考，但不是核心定义）：涉及多文件、跨模块。
注意「改 100 个文件的机械替换」未必需要 Change，而「改 1 个文件却改变安全语义」很可能需要。

其他明确场景：

- 引入/调整架构、模块边界、技术选型。
- 需要记录取舍与验收依据，供后续回溯。
- 简化/重构既有结构，且存在被质疑或回退的可能。

> Change 的类型与状态不写在 `change.md` 内，而以目录路径（`proposed/feature/` 等）为唯一事实源。提交 Change 时把它放进对应目录即可，无需在文件里标 Type / Status。

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
├── proposed/      # 按类型再分；每个 Change 一个独立目录，实际产生 Change 时创建
├── implemented/
├── rejected/
├── archived/
└── templates/     # 模板，非实际 Change
```

每个 Change 始终以独立目录存在，`change.md` 为唯一必选主文档；`Spec / Research / Design / Plan` 按需作为同目录下的附件加入。不存在「单文件 Change」形态，也不存在后续文件升级目录的迁移动作。

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

`change.md` 是核心文件，其余（Spec / Research / Design / Plan）全部按需创建。Change 从创建到归档始终保持 `<date>-<slug>/change.md` 这一内部结构；新增 Supplemental Documents 不改变主文档结构，生命周期流转仅改变其所在的状态目录（`proposed/ → implemented/ → archived/`）。
不需要为保留目录而批量制造 `.gitkeep`。

### 类型与状态的唯一事实源

**Change 的类型与生命周期状态以目录路径为唯一事实源，不在 `change.md` 中重复维护。**

```text
proposed/feature/
         │       │
         │       └── 类型（Type）
         └────────── 状态（Status）
```

文件在 `proposed/ → implemented/ → archived/` 或 `proposed/ → rejected/` 之间移动时，状态自然改变，无需修改 `change.md` 内的字段。

### `change.md` 精确必选结构

下列代码格式名称是实例必须使用的精确标题，所有必选章节都必须包含实际内容：

| 状态 | 必选二级标题 | 额外必选标题 |
| --- | --- | --- |
| 全部状态 | `## 概要`、`## 问题`、`## 目标与范围` | — |
| `proposed` | `## 方案`、`## 验收标准` | — |
| `implemented` | `## 最终决策`、`## 验证结果` | 不再保留 `## 方案`、`## 验收标准` |
| `rejected` | `## 方案`、`## 验收标准`、`## 拒绝状态补充` | `### 拒绝原因` |
| `archived` | `## 最终决策`、`## 验证结果`、`## 归档状态补充` | `### 归档原因`；不再保留 `## 方案`、`## 验收标准` |

### 文档语言约定

- **面向人的文档标题与说明默认使用中文**。
- **文件名、目录名、枚举值、标准协议术语保留英文**：如 `change.md`、`spec.md`、`proposed`、`feature`、`REQ-001`、`API`、`Given / When / Then`、`Benchmark` 等。
- 描述具体文件类型时保留英文标识（如 `Spec / Research / Design / Plan`）；普通自然语言描述可写中文（规格、调研、设计、实施计划）。

---

## 7. 五种文档各自职责

| 文档 | 职责 | 不写什么 |
|------|------|----------|
| `change.md` | 一次变更的主记录：为什么变、总体变什么、关键取舍、验收、最终决策 | 冗长的技术调研过程 |
| `spec.md` | 系统必须表现出的行为，以及如何验证行为正确 | 代码结构、具体实现设计、实施任务 |
| `research.md` | 解决影响设计的重要技术未知，为 Design 提供可靠输入 | 最终技术设计本身 |
| `design.md` | 为满足 Change/Spec 最终采用的技术方案 | 复制 Spec、任务清单、未收敛的调研过程 |
| `plan.md` | 把已确定的设计转成有顺序、有依赖、有验证方式的实施路径（兼任务拆分 Task Breakdown） | — |

> Change 是中心；Spec / Research / Design / Plan 都是**按需附件**，不是固定流水线。
> 简单变更可能只有 `change.md` 即可。

---

## 8. 补充文档（Supplemental Documents）的创建条件

当某个 Change 需要专项文档承载时，按需拆出补充文档。判断标准是文档是否「有必要存在」，而非篇幅大小：

- `spec.md`：行为、业务规则、状态或验收场景复杂，需要独立描述。
- `research.md`：存在影响决策的重要未知，需要调查、实验或验证。
- `design.md`：存在值得显式记录的重要技术设计或取舍。
- `plan.md`：实施涉及多个步骤、阶段、模块、迁移或明显前后依赖。

> 一个方案可能只有几十行，但涉及数据一致性、模块边界、对外契约或安全策略，同样值得写 Design；反之篇幅长不等于必须拆出。

这些文档跟随所属 Change 目录一起在生命周期中流转，**不建立独立生命周期**。
本阶段不创建独立的 `tasks.md`；仅当未来出现超大型任务、多 Agent 并行或独立状态跟踪需求时再考虑拆出。

---

## 9. 禁止重复维护同一信息

- 同一事实只应在**最合适的一篇文档**中作为权威来源。
- 其他文档引用它，而不是复制它。例如：`design.md` 引用 `spec.md` 的需求编号，而非重写需求。
- 状态流转（proposed → implemented 等）时，更新文档语义（如 方案 → 最终决策），而非在多处追加历史说明。

---

## 10. Change 完成 / 拒绝 / 归档的处理

- **实现完成**：将 Change 目录从 `proposed/` 移至 `implemented/`；核心文件 `change.md` 语义从「计划」转为「实际决策」
  （方案 → 最终决策，验收标准 → 验证结果，风险与约束 → 影响与后果）。
- **拒绝**：移至 `rejected/`；保留原方案并记录拒绝原因。
- **归档**：移至 `archived/`；记录为何归档、被哪个新 Change 替代（若存在）。

所有移动为显式操作，由用户或 Coding Agent 决定，无自动触发机制。

---

## 11. Change 与 Postmortem 的关系

Postmortem 的定义、触发条件、命名、内容边界和模板统一以 [`docs/postmortem/README.md`](../postmortem/README.md) 为唯一权威来源，本文件不重复维护。

二者回答不同问题：

```text
已发生且逃过防线的问题
        ├─ Postmortem：为什么发生、为什么防线没工作、要补什么 Guardrail
        └─ bug-fix / process / testing Change：准备怎样修、行为如何变化、如何验收
```

同一问题可以同时产生一份 Postmortem 和一个或多个 Change。Postmortem 中的 Guardrail 应链接到负责落地的 Change；Change 只记录整改方案、最终决策与验证结果，不复制事故分析正文。普通 Bug 未达到 Postmortem 触发条件时，只创建必要的 bug-fix Change。

---

## 12. 文档关系与目录架构

```text
④ Change ───────────── 一次有意义的系统改变
        ├── ⑤ Spec      正确行为
        ├── ⑤ Research  消除未知
        ├── ⑤ Design    技术方案
        └── ⑤ Plan      落地路径

⑥ Postmortem ───────── 已发生的系统性失败
        │
        ▼
    找出防线缺口
        │
        ▼
    产生新的 Change（Guardrails 落地）
```

### 12.1 最终目录架构

```text
docs/
├── changes/                       # Change + Supplemental
│   ├── README.md                  # Change 生命周期与治理规则
│   ├── proposed/      <type>/<date>-<slug>/
│   ├── implemented/   <type>/<date>-<slug>/
│   ├── rejected/      <type>/<date>-<slug>/
│   ├── archived/      <type>/<date>-<slug>/
│   └── templates/                 # Change/Spec/Research/Design/Plan 模板
│
└── postmortem/                    # 事后分析（无生命周期目录）
    ├── README.md
    ├── templates/
    │   └── postmortem.md
    └── <date>-<slug>.md
```

### 12.2 每个文件的必选 / 可选 + 创建条件

| 文档 | 必选/可选 | 创建条件 | 归属 |
|------|-----------|----------|------|
| `change.md` | **必选**（每个 Change 至少一个） | 改变系统行为 / 契约 / 架构，或有重要设计决策、以后需知「为什么这样改」 | ④ Change |
| `spec.md` | 可选 | 行为 / 业务规则 / 状态 / 验收复杂需独立描述 | ⑤ Spec |
| `research.md` | 可选 | 存在影响决策的重要未知，需调查 / 实验 / 验证 | ⑤ Research |
| `design.md` | 可选 | 存在值得显式记录的重要技术设计或取舍 | ⑤ Design |
| `plan.md` | 可选 | 实施涉及多步骤 / 阶段 / 模块 / 迁移 / 前后依赖 | ⑤ Plan |
| `postmortem.md` | **必选**（每篇 Postmortem 一个） | 满足 [`docs/postmortem/README.md`](../postmortem/README.md) 定义的触发条件 | Postmortem |

> 类型与状态以**目录路径为唯一事实源**（Change）；Postmortem 无状态流转，仅按日期归档。

### 12.3 创建条件速查

- **改 100 个文件的机械替换** → 未必需要 Change。
- **改 1 个文件却改变安全语义** → 很可能需要 Change。
- **普通 Bug** → 创建必要的 bug-fix Change；是否另建 Postmortem 按其[唯一规范](../postmortem/README.md)判断。
- 判断不清是否创建 Change 时，倾向创建仅含 `change.md` 的轻量记录。

---

## 13. 治理规则（长期适用，不新增文件）

以下规则让本体系从「文档结构设计得不错」升级为「适合长期给 Coding Agent 使用的知识系统」。它们不引入新文档类型，只约束现有文档的维护与互链方式。

### 13.1 Implemented 是活的当前决策，而非死历史

`implemented/` 下的 Change 是**当前仍然有效的决策事实**，不是归档后即冻结的档案。

- **实现事实变化**（路径、类名、配置名、默认值、关键机制等非决策性变化）→ **同步更新原 implemented Change**，不要靠不断追加历史叙述来记录变化。
- **原有设计决策被推翻**（决策本身反转）→ **创建新的 Change**，不得把旧 Change 改写成相反意思；新旧 Change **必须相互引用**（旧 Change 标注 `Superseded By`，新 Change 标注 `Supersedes`）。
- 否则数年后 `implemented/` 会变成「当年对、现在半错」的文档堆。

### 13.2 Research 必须标注证据等级

见 [`templates/research.md`](./templates/research.md) 的「证据等级」小节。核心约束：

- 每条影响设计的关键结论标注 `Verified` / `Documented` / `Assumed`。
- **承重结论**（决定架构、数据格式、兼容性、安全、一致性）不应停留在 `Assumed`；高风险时也不应只停留在 `Documented`（应 Spike / PoC 升级为 `Verified`）。
- 禁止用本 Research 自身作为自身证据（自引用）。

### 13.3 关键结论须有外部证据

- 会直接决定架构、数据格式、兼容性、安全、一致性的结论，不能只靠二手描述或 AI 自信推断。
- 高风险承重结论必须落到 `Verified` 级别（源码 / 实验 / 测试 / 实际运行），而非停留在 `Documented` 或 `Assumed`。

### 13.4 文档之间必须使用真实相对链接

所有文档互引用**真实 Markdown 相对链接**，禁止「见 2026-08-19-xxx」「参考之前的 Design」「Change #17」这类口头/裸引用。

```markdown
详见 [文档版本设计](./design.md)
由 [wrong-session-validation Postmortem](../../../../postmortem/2026-08-23-wrong-session-validation.md) 触发。
```

应可被机械校验的链接关系（不准断链）：

- Change → Spec / Research / Design / Plan
- Design → Research（若引用）
- Postmortem → 由其催生的 Change
- Archived Change → Superseding Change

### 13.5 proposed → implemented 的完成 Gate

将 Change 从 `proposed/` 移至 `implemented/` 前，必须完成一次“移动前预检”，确认以下事项全部成立；移动目录后还必须执行一次“移动后终检”。两次校验都通过后，才能提交。

1. 实际实现与最终 Decision 一致。
2. Acceptance 已转换为真实 Verification（有证据）。
3. Spec 中不存在影响正确性的未决问题。
4. Research 中影响设计的关键假设已得到处理（或显式记录残留风险）。
5. Design 描述的是最终实现，而非废弃方案。
6. Plan 与最终实现存在重要偏差时已更新。
7. 相关测试 / 构建 / 验证已经通过。
8. 文档之间不存在明显矛盾或失效链接。

9. `change.md` 的正文已完成生命周期语义转换：不再把当前决策、已完成验证写成计划或将来时；正文中的当前 Change 链接、状态路径和章节名称与 `implemented/` 目录一致。历史过程描述可以保留，但必须明确标注为历史，不得造成当前状态歧义。

移动前预检至少运行：

```text
python knowledge/scripts/validate.py
git diff --check
```

完成目录移动和正文转换后，必须再次运行同样的完整校验；若终检失败，不得提交该生命周期移动。

> 满足 Gate 才移动目录；这不是「挪个目录就算完成」。

### 13.6 Archive 冻结且不再是当前权威；备选方案有则必录

- `archived/` = **曾经有效、但已不是当前事实源**的历史决策。原则上不再更新内容；发现问题优先通过当前 Change / `knowledge/` 纠正，而非持续维护历史档案。
- 每个 archived Change 应尽量链接 `Superseded By: <新 Change>`；Agent 查到旧设计时不会误当作现在架构。
- **备选方案**（见 [`templates/change.md`](./templates/change.md)）：存在真实备选或明显取舍时**必须记录**；没有真实备选时**删除本节**，禁止为模板完整虚构方案。

### 13.7 职责越界优先拆 Supplemental，而非加篇幅

文档只拥有属于自己的事实。发现某份文档持续变长时，先检查是否职责越界（如 Change 写了 Design 细节），应拆出对应 Supplemental 文档，而不是提高篇幅上限。当前阶段不设置机械字数预算；待知识库规模真正起来后再评估。
