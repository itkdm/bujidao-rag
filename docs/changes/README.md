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

### 类型与状态的唯一事实源

**Change 的类型与生命周期状态以目录路径为唯一事实源，不在 `change.md` 中重复维护。**

```text
proposed/feature/
         │       │
         │       └── 类型（Type）
         └────────── 状态（Status）
```

文件在 `proposed/ → implemented/ → archived/` 或 `proposed/ → rejected/` 之间移动时，状态自然改变，无需修改 `change.md` 内的字段。

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

- **实现完成**：将目录从 `proposed/` 移至 `implemented/`；`change.md` 语义从「计划」转为「实际决策」
  （方案 → 最终决策，验收标准 → 验证结果，风险与约束 → 影响与后果）。
- **拒绝**：移至 `rejected/`；保留原方案并记录拒绝原因。
- **归档**：移至 `archived/`；记录为何归档、被哪个新 Change 替代（若存在）。

所有移动为显式操作，由用户或 Coding Agent 决定，无自动触发机制。

---

## 11. Postmortem（事后分析）的定位与边界

> Postmortem 不是 Change，也不是 Agent Note。它针对**已经发生、并且逃过了现有防线**的问题做事后分析。
> 核心问题始终是：**为什么这个问题能够发生并逃过现有防线，以及以后如何让同类问题更早、更响亮地失败。**

### 11.1 它负责什么、不负责什么

它**不负责**：

```text
怎么修这个 Bug              → bug-fix Change
准备采用什么新方案          → Change / Design
具体开发步骤                → Plan
```

它**负责**：

```text
发生了什么？
真正根因是什么？
为什么测试没发现？
为什么 Review 没发现？
为什么 CI / 类型系统 / 规范没有阻止？
以后增加什么 Guardrail？
```

### 11.2 比 Change 更「克制」——不写「每修一个 Bug 就写复盘」

Postmortem 的触发**不单纯看事故严重度**，而看三个维度是否同时满足（至少满足其一即建议写）：

| 维度 | 含义 | 信号示例 |
|------|------|----------|
| 隐蔽性 | 原因不容易想到、根因反直觉 | 调试数小时才定位；看似正确的验证对象其实是错的 |
| 系统性 | 防线存在缺口、机制导致隐蔽故障 | 测试覆盖了「看起来相同」的场景却测错对象；CI 存在却没发现 |
| 复现成本 | 下次重新踩坑代价高 | 同类问题反复出现；安全 / 数据一致性 / 发布流程类故障；Agent 极易再次犯同类错误 |

**应该写**（典型场景）：

- Bug 已进入生产环境 / 已合并到主分支或发布版本
- CI 明明存在却没有发现
- 测试覆盖了「看起来相同」的场景，却测试错对象
- 某架构 / 工具机制导致隐蔽故障
- 同类问题反复出现
- 调试了很久、根因极其反直觉
- 安全、数据一致性、发布流程等系统性故障
- Agent 非常容易以后再次犯同类错误

**不应该写**（工程防线已正常工作，无需复盘）：

- `NullPointerException`：原因是忘记判空
- 变量写错、普通接口返回字段错误
- 依赖版本升级导致的简单兼容问题（修掉即可）
- 测试已经正常失败并阻止合并

> 经验法则：Postmortem 关心的是**「为什么防线没有工作」**，而不是「Bug 怎么修」。如果防线正常工作，通常不写。

### 11.3 与 bug-fix Change 的关系

同一事故可同时产生 **Postmortem + 一个或多个 Change**，二者回答完全不同的问题：

```text
生产环境任务重复执行
        │
        ▼
调查发现：分布式锁失效
        │
        ├───────────────┐
        ▼               ▼
 Postmortem         bug-fix Change
 为什么没挡住        怎么修当前问题
```

- **Postmortem**：为什么锁失效？单测为何没测出？集成测试为何没覆盖多实例？Review 为何没发现？以后怎么防止同类错误？
- **bug-fix Change**：准备怎样修？采用什么新机制？行为怎么变化？怎么验收？

### 11.4 必须导向 Guardrails，而非「总结经验」

Postmortem 的产出不能是泛泛的「以后要更细心 / 加强测试 / 提高责任心」，而是要变成具体的、让工程系统替人记住事故的防线：

```text
Guardrail 1  新增并发集成测试
Guardrail 2  CI 强制运行该测试
Guardrail 3  AGENTS.md 增加：修改 xxx 时必须验证多实例行为
Guardrail 4  增加静态检查 / 脚本
```

> 核心思想：**不要依赖人记住事故，要让工程系统记住事故。** 每条 Guardrail 应明确其落地形式（Test / CI / Rule / Tooling）与对应 Change 链接。

### 11.5 内容边界（先定架构，模板后补）

```text
postmortem.md
│
├── Executive Summary
│
├── Impact / What Happened
│
├── Timeline（推荐，但允许简化）
│
├── Root Cause
│
├── Why It Escaped
│   ├── Tests
│   ├── Review
│   ├── Tooling / CI
│   └── Process / Rules
│
├── Guardrails
│
└── Related Changes
```

最重要的是 **Root Cause + Why It Escaped + Guardrails** 三块。Timeline 比传统 SRE Postmortem 更轻：

- 大型线上事故可记精确时间线（发布 / 报错 / 告警 / 定位 / 回滚 / 根因确认）。
- 普通隐蔽 PR Bug 可简化：发现 → 初步误判 → 排查 → 根因确认 → 修复。

### 11.6 无生命周期目录

Postmortem 描述的是**已经发生过的历史事实**，本身不需要 `proposed/implemented/archived` 流转。独立目录即可：

```text
docs/postmortem/
├── README.md
├── 2026-08-23-wrong-session-validation.md
└── 2026-08-24-lock-failure-in-multi-instance.md
```

命名沿用 Change 的 `日期 + slug` 风格；序号（如 `0001-`）可选，默认用日期更利于追溯。

---

## 12. ④⑤⑥ 完整关系与封板

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

```text
                    发生问题
                       │
                       ▼
                普通 Bug 吗？
                  │          │
                 是          否/存在系统性价值
                  │          │
                  ▼          ▼
           bug-fix Change   Postmortem
                  │          │
                  │      找根因 + 防线缺口
                  │          │
                  │          ▼
                  │       Guardrails（Test/CI/Rule/Tooling）
                  │          │
                  └──────┬───┘
                         ▼
                    Change(s) 实施整改
```

### 12.1 最终目录架构

```text
docs/changes/
├── README.md                 # ④⑤⑥ 总规范（本文件）
├── proposed/      <type>/<date>-<slug>/   # 讨论/实施中 Change
├── implemented/   <type>/<date>-<slug>/   # 已验证 Change
├── rejected/      <type>/<date>-<slug>/   # 未采用
├── archived/      <type>/<date>-<slug>/   # 已失效/被替代
├── templates/                     # Change/Spec/Research/Design/Plan 模板
└── docs/postmortem/               # ⑥ 事后分析（无生命周期目录）
    ├── README.md
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
| `postmortem.md` | **必选**（每篇 Postmortem 一个） | 问题已发生且逃过防线，且满足隐蔽性 / 系统性 / 复现成本任一维度 | ⑥ Postmortem |

> 类型与状态以**目录路径为唯一事实源**（Change）；Postmortem 无状态流转，仅按日期归档。

### 12.3 创建条件速查

- **改 100 个文件的机械替换** → 未必需要 Change。
- **改 1 个文件却改变安全语义** → 很可能需要 Change。
- **普通 Bug，防线正常工作** → bug-fix Change 即可，不写 Postmortem。
- **Bug 逃过防线且根因反直觉 / 系统性强 / 复现成本高** → Postmortem + 相关 Change。
- 判断不清时，倾向创建轻量 Change（仅 `change.md`）；Postmortem 则倾向「更克制」，宁可少写。
