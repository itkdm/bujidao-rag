---
# ==================== 知识库控制文件（基础设施） ====================
# 本文件属于知识库基础设施，不受"知识文件必须套模板"约束。
# 基础设施文件清单：KNOWLEDGE-RULES.md / ROUTING.md / README.md / INDEX.md / template/
id: KB-INFRA-KNOWLEDGE-RULES
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
- convention
- knowledge-base
anchors:
- GLOBAL:KNOWLEDGE-RULES
---

# 知识库全局维护规则（KNOWLEDGE-RULES）

> **⚠️ 团队规定：此文件为必选文件，且为最高优先级规范。**
> 所有写入、读取、修改 `knowledge/` 目录下知识的行为（无论开发者还是 AI），都必须遵守本文件。
> 当本文件与各类型模板（template/）发生冲突时，**以本文件为准**。

---

## 一、文件定位

| 维度 | 说明 |
|------|------|
| 本文件是什么 | 知识库的全局规则文件，定义公共字段规范、目录归属规则、流转机制、AI 读取约束 |
| 本文件不是什么 | 不是某个应用的知识文档，不是业务说明，不是 ROUTING 路由表 |
| 谁必须遵守 | 所有团队成员 + 所有 Coding Agent + 所有 AI 辅助工具 |
| 与其他文件的关系 | `template/` 下的模板是"类型级强约束"，本文件是"全局级强约束"；模板不得违反本文件 |

---

## 二、文件分类：知识文件 vs 基础设施文件

知识库中的文件分为两类，适用不同的规则体系。

### 2.1 知识文件

知识文件是知识库的核心内容，**必须严格遵守 Front Matter + 模板规范**。

| 目录 | 说明 |
|------|------|
| `main/` | 跨应用通用知识 |
| `applications/` | 应用级知识 |
| `candidate/` | 候选知识 |
| `personal/` | 个人知识 |

### 2.2 基础设施文件

基础设施文件是知识库的运行框架，**不受"知识文件必须套模板"约束**，采用本文件定义的元规则。

| 文件/目录 | 说明 |
|-----------|------|
| `KNOWLEDGE-RULES.md` | 全局规则（本文件） |
| `ROUTING.md` | 知识检索路由表 |
| `README.md` | 知识库定位说明 |
| `INDEX.md` | 全局索引 |
| `template/` | 写作模板目录 |

基础设施文件不要求 `type` 字段，不要求套用模板，但必须包含本文件定义的公共 Front Matter 字段（见第三章）。

### 2.3 为什么这样区分

如果所有文件都要求套模板，会产生自举悖论：

- `KNOWLEDGE-RULES.md` 用哪个模板？
- `template/` 下的模板自己套哪个模板？
- 最终必然出现 `template-template` 这种套娃问题。

明确区分两类文件后，规则体系干净且无循环依赖。

---

## 三、公共 Front Matter 字段规范

### 3.1 知识文件必填字段

| 字段 | 类型 | 必填 | 取值范围 / 格式 | 说明 |
|------|------|------|----------------|------|
| `id` | string | ✅ | `KB-{TYPE}-{DOMAIN}-{SEQ}` | 知识唯一编号，全局不重复 |
| `type` | string | ✅ | 见 3.2 | 知识对象类型，对应 `template/` 下模板 |
| `scope` | string | ✅ | `cross-app` / `{appCode}` | 适用范围：全局或指定应用 |
| `status` | enum | ✅ | `DRAFT` / `CANDIDATE` / `OFFICIAL` / `DEPRECATED` | 知识生命周期状态 |
| `authorship` | enum | ✅ | `human` / `ai-assisted` / `mixed` | 生成方式（见 3.3） |
| `owner` | string | ✅ | 团队名或 userId | 长期责任主体（见 3.4） |
| `maintainers` | list | ❌ | userId 列表 | 当前维护人列表 |
| `version` | integer | ✅ | 从 1 开始 | 版本号（见 3.5） |
| `updatedAt` | date | ✅ | `YYYY-MM-DD` | 文件最后编辑时间 |
| `verifiedAt` | date | ✅ | `YYYY-MM-DD` | 内容最后与真实来源核对的时间（见 3.6） |
| `confidence` | enum | ✅ | `high` / `medium` / `low` | 置信度 |
| `stability` | enum | ✅ | `stable` / `evolving` / `volatile` | 稳定性 |
| `evidence` | list | ✅ | 见 3.7 | 证据来源 |
| `tags` | list | ✅ | 自由标签，至少 1 个 | 检索分类用 |
| `anchors` | list | ❌ | `{TYPE}:{value}` 格式 | 锚点，供 ROUTING 路由匹配（见 3.8） |

### 3.2 type 取值对照表

| type 值 | 对应模板 | 存放目录 |
|---------|----------|----------|
| `application` | `template/application-template.md` | `applications/{app}/` |
| `tech` | `template/tech-template.md` | `main/tech/` 或 `applications/{app}/tech/` |
| `rule` | `template/rule-template.md` | `main/rules/` 或 `applications/{app}/domain/rule/` |
| `flow` | `template/tech-template.md` | `applications/{app}/domain/product/` 或 `domain/solution/` |
| `state` | `template/tech-template.md` | `applications/{app}/domain/product/` 或 `main/states/` |
| `base` | `template/base-template.md` | `applications/{app}/domain/base/` |
| `glossary` | `template/tech-template.md` | `main/glossary/` |

> **注意**：`type` 只描述知识内容类型，不描述文件位置或状态。基础设施文件（见 2.2）不需要 `type` 字段。

### 3.3 authorship：生成方式

`authorship` 描述知识内容的生成方式，与 `status` 正交：

| 值 | 含义 |
|----|------|
| `human` | 完全由人工编写 |
| `ai-assisted` | AI 辅助生成，人工审核确认 |
| `mixed` | 人工与 AI 协作编写 |

**关键原则**：`authorship` 与 `status` 相互独立。一篇 `authorship: ai-assisted` 的知识经过 owner 审核后，`status` 可以是 `OFFICIAL`。`OFFICIAL` 表示"当前正式有效"，不表示"纯人工编写"。

### 3.4 owner 与 maintainers

| 字段 | 含义 | 示例 |
|------|------|------|
| `owner` | 长期责任主体，通常是团队名 | `backend-platform` / `order-team` |
| `maintainers` | 当前具体维护人列表 | `[user123, user456]` |

**为什么区分**：全局规范（如 Git Commit 规范、知识库规则）是团队资产，不是某个人的资产。使用团队名作为 owner 可以避免人员转岗时大量文档需要修改 owner。

### 3.5 version 递增规则

**统一原则：所有语义变更 version +1，纯格式变更 version 不变。**

| 操作 | version | updatedAt | verifiedAt |
|------|---------|-----------|------------|
| 正文实质修改 | +1 | 更新 | 视情况更新 |
| 证据更新 | +1 | 更新 | 更新 |
| 状态流转（任何方向） | +1 | 更新 | 视情况更新 |
| owner / maintainers 变更 | +1 | 更新 | 不变 |
| 仅修正错别字、空格、换行 | 不变 | 更新 | 不变 |
| Markdown 排版调整 | 不变 | 更新 | 不变 |

**没有例外**：`OFFICIAL → DEPRECATED` 也是状态变化，必须 `version +1`。

### 3.6 updatedAt vs verifiedAt

| 字段 | 含义 | 更新时机 |
|------|------|----------|
| `updatedAt` | 文件最后编辑时间 | 任何编辑操作后 |
| `verifiedAt` | 内容最后与真实来源（代码/需求/系统）核对的时间 | 仅在与真实来源核对后 |

**为什么区分**：假设代码最后核对是 2026-07-01，8 月 17 日只是修了个标点。如果只有 `updatedAt: 2026-08-17`，Agent 可能误以为 8 月 17 日刚和代码核对过。`verifiedAt` 明确区分"编辑时间"和"验证时间"。

### 3.7 evidence 结构规范

```yaml
evidence:
- type: code
  ref: "com.xxx.service.OrderService#createOrder"
  verifiedAt: 2026-08-17
- type: doc
  ref: "内部 Wiki 链接"
- type: human
  ref: "张三/2026-08-15/需求评审会议"
```

| type | 含义 |
|------|------|
| `code` | 代码路径或核心模块路径，必须有具体路径 |
| `doc` | 文档链接（内部 Wiki / RFC / ADR） |
| `human` | 人工确认记录（确认人/时间/方式） |

### 3.8 anchors 唯一性规则

`anchors` 用于 ROUTING 路由匹配。规则如下：

- **允许**多个知识文件拥有相同 anchor（一个业务概念可能关联多个知识文件）
- **必须**由 `ROUTING.md` 明确优先级，避免 Agent 不知道该读哪个
- 如果两个文件 anchor 相同且优先级相同，ROUTING 必须列出两者并说明适用场景

---

## 四、目录职责与内容归属规则

### 4.1 核心目录归属判定

| 目录 | 放什么 | 不放什么 | 归属判定标准 |
|------|--------|----------|--------------|
| `main/` | 跨应用、跨系统、跨业务线的通用知识 | 单应用内部实现细节 | 放到某个应用目录下会导致其他应用检索时漏掉 → 进 main |
| `applications/` | 应用范围内的知识 | 全局通用概念 | 只服务于单个应用 → 进 applications |
| `candidate/` | 待确认候选知识 | 已确认的正式知识 | AI 分析出的推断、未经 owner 确认的内容 |
| `personal/` | 个人经验和踩坑记录 | 团队正式结论 | 个人工作区，验证后可转 candidate |
| `template/` | 各类文档的写作模板 | 实际知识内容 | 只放模板，不放数据 |
| `archive/` | 已废弃或过期知识的归档副本 | 活跃知识 | 仅用于历史追溯，不进入正常路由 |

### 4.2 main/rules/ vs main/tech/ 的明确区分

| 目录 | 放什么 | 示例 |
|------|--------|------|
| `main/rules/` | 开发、协作、交付、知识管理等**强制规范** | Git Commit 规范、分支规范、Code Review 规范、版本发布规范、知识库规范、安全红线 |
| `main/tech/` | 跨应用共享的**技术知识和技术约束** | Java 编码约定、Spring Boot 通用实践、Redis 使用规范、MQ 通用约束、异常处理技术约定 |

**判断标准**：
- 是"必须遵守的协作/流程规范" → `main/rules/`
- 是"技术实现层面的通用约束" → `main/tech/`

### 4.3 applications/ 内部结构规则

```
applications/{app}/
├── application-{app}.md    # 应用总览（必须有）
├── INDEX.md                # 应用内导航（必须有）
├── domain/
│   ├── product/            # 主干能力，稳定，写"做什么"
│   ├── solution/           # 差异化方案，写"差异是什么"
│   ├── rule/               # 应用级业务规则
│   └── base/               # 接口/消息/模型/Repository 索引
└── tech/                   # 应用级技术约束
```

**强制约束**：
- `solution/` 下**禁止复制** `product/` 全流程，只写差异部分
- `base/` 只做索引（指向代码路径），不展开实现细节
- AI 读取顺序：应用总览 → INDEX → product → solution → rule → base → tech → 回到代码

### 4.4 candidate/ 目录结构

`candidate/` 镜像正式目录结构，便于晋升时自然迁移：

```
candidate/
├── main/
│   ├── rules/
│   └── tech/
└── applications/
    ├── {app1}/
    └── {app2}/
```

晋升路径示例：`candidate/applications/order/domain/product/xxx.md` → `applications/order/domain/product/xxx.md`

---

## 五、status 流转规则

### 5.1 状态定义

| 状态 | 含义 |
|------|------|
| `DRAFT` | 草稿，内容不完整或未经过初步验证 |
| `CANDIDATE` | 候选，内容完整，有初步证据，等待 owner review |
| `OFFICIAL` | 正式，经 owner 确认，可作为稳定上下文使用 |
| `DEPRECATED` | 已废弃，内容过期或错误，保留历史但不进入正常路由 |

### 5.2 流转路径

```
DRAFT ──→ CANDIDATE ──→ OFFICIAL ──→ DEPRECATED
  ↑                        │
  └────────────────────────┘ (发现错误，重新确认)
```

| 流转 | 条件 | 操作人 |
|------|------|--------|
| DRAFT → CANDIDATE | 知识内容完整，有初步证据，准备提交 review | 作者 |
| CANDIDATE → OFFICIAL | owner 确认内容准确、稳定、证据充分 | owner |
| OFFICIAL → DEPRECATED | 代码或业务变化导致知识过期/错误 | owner 或需求负责人 |
| OFFICIAL → DRAFT | 发现重大错误需重写（极少发生，优先 DEPRECATED + 新建） | owner |

### 5.3 目录与 status 的匹配规则

| 目录 | 允许的状态 |
|------|-----------|
| `main/` | `OFFICIAL` / `DEPRECATED` |
| `applications/` | `OFFICIAL` / `DEPRECATED` |
| `candidate/` | `DRAFT` / `CANDIDATE` |
| `personal/` | `DRAFT` / `CANDIDATE` |

**关键设计**：
- `main/` 和 `applications/` **允许 DEPRECATED**，原地标记，不移动到 `archive/`。原因：移动文件会导致大量链接失效。
- `candidate/` **允许 DRAFT**。团队成员准备写新的团队级知识时，第一版 DRAFT 可以直接放 `candidate/`，不必先放 `personal/`。
- `personal/` 只表达"这是个人知识，不代表团队结论"，与生命周期状态（DRAFT/CANDIDATE）正交。

### 5.4 DEPRECATED 的处理规则

- DEPRECATED 文件**原地保留**，`status: DEPRECATED`，不移动目录
- ROUTING 默认**只索引 OFFICIAL**，DEPRECATED 不进入 Agent 正常检索结果
- 需要追溯历史时，可显式指定读取 DEPRECATED 文件
- 文件顶部必须添加醒目提示：`> ⚠️ 本文档已废弃，请勿作为事实引用`
- 禁止删除 DEPRECATED 文件（除非极端情况且经 owner 确认）

---

## 六、知识流转与回补规则

### 6.1 正向流转路径

```
personal/ 个人经验
    ↓ （验证后）
candidate/ 候选知识（状态 DRAFT → CANDIDATE）
    ↓ （owner review + 确认稳定性）
main/ 或 applications/ 正式知识（状态 OFFICIAL）
```

### 6.2 需求执行中的回补路径

```
需求执行 → AI 分析出有价值信息 → 写入 candidate/（标清来源、可信度、待确认项）
    ↓ （需求发布后）
owner/研发同学 review candidate/ → 确认稳定 → 合并到 main/ 或 applications/ → 状态改为 OFFICIAL
```

### 6.3 禁止事项

| 禁止行为 | 原因 |
|----------|------|
| AI 直接将未确认内容写入 `main/` 或 `applications/` | 错误知识比没有知识更危险 |
| AI 将 personal 经验直接当作团队结论引用 | personal 未经验证，不代表团队共识 |
| 人工跳过 candidate 直接写 OFFICIAL | 缺少证据追溯，后续难维护 |
| 删除 DEPRECATED 文件 | 删除会丢失历史变更记录 |

---

## 七、模板使用规范

### 7.1 强制约束

- `template/` 下的模板是**强约束，不是建议格式**
- AI 在 `knowledge/` 下写入**知识文件**时，**必须套用对应类型的模板**
- 禁止 AI 自行发明新的文档结构或省略 Front Matter 字段
- 当某个类型没有对应模板时，AI 必须**先创建模板**（放入 `template/` 并经 owner 确认），再写入知识

### 7.2 模板与公共字段的关系

- 各类型模板的 Front Matter **必须包含本文件第三章定义的所有公共字段**
- 各类型模板可以**追加本类型特有字段**（如 `application` 类型追加 `domain`、`appType`）
- 模板中公共字段的取值说明可以引用本文件，不需要在模板中重复定义

### 7.3 基础设施文件不受模板约束

`KNOWLEDGE-RULES.md`、`ROUTING.md`、`README.md`、`INDEX.md` 和 `template/` 下的文件属于基础设施，不要求套用模板。

---

## 八、易变信息处理规则（核心原则）

> **KB 提供稳定上下文，当前代码仍然是实现事实。**

### 8.1 只做定位入口的信息类型

以下内容即使在知识库中被提及，也**只作为定位入口**（指向代码路径），AI 在编码前**必须回到当前仓库核对真实代码**：

| 信息类型 | 示例 |
|----------|------|
| 接口签名 | 方法名、参数列表、返回值类型 |
| DTO 字段 | 请求/响应对象的字段定义 |
| Topic 配置 | MQ 的 Topic 名称、Tag、Group |
| feature key / 开关值 | 功能开关的 key 和默认值 |
| 状态枚举 | 具体的枚举值和含义 |
| 表结构字段 | 数据库表的列名、类型 |

### 8.2 定位入口的写法规范

在知识文件中提及上述易变信息时，必须包含：
1. **代码路径**（如 `com.xxx.service.OrderService#createOrder`）
2. **说明这是定位入口**（如用 `(定位入口，编码前请核对代码)` 标注）
3. **最后核对时间**（在 `verifiedAt` 字段中体现）

---

## 九、AI 读取与路由规范

### 9.1 两个入口，两种场景

知识库有两个入口文件，分别服务于不同场景：

| 场景 | 入口文件 | 说明 |
|------|----------|------|
| **会话级初始化** | `KNOWLEDGE-RULES.md` | 首次接触知识库时读取，理解全局规则 |
| **需求级检索** | `ROUTING.md` | 每个具体需求开始时读取，定位目标知识 |

**关键区别**：
- `KNOWLEDGE-RULES.md` 是"规则入口"——告诉 AI 知识库怎么用
- `ROUTING.md` 是"知识检索入口"——告诉 AI 具体需求该读哪些知识

### 9.2 渐进式加载顺序

```
会话首次接触知识库：
  1. 读取 KNOWLEDGE-RULES.md（理解规则）

每个具体需求：
  1. 读取 ROUTING.md（定位）
  2. 按路由结果进入 main/ 或 applications/ 下的具体文件
  3. 如需了解知识库整体结构 → 读 README.md
  4. 最后 → 回到当前应用仓库核对代码
```

### 9.3 复用规则

如果 Agent 已在当前会话中加载过 `KNOWLEDGE-RULES.md` 的当前版本，无需重复读取。每个需求只需读取 `ROUTING.md` 进行定位。

### 9.4 上下文窗口管理

- AI 不应一次性加载超过需求所需的上下文
- 优先加载：应用总览 → 相关 flow → 相关 state → 相关 rule
- 延迟加载：跨应用流程、全局术语（仅在涉及时才读取）

---

## 十、变更同步规则

### 10.1 触发条件

当发生以下任一情况时，相关知识的负责人必须在**需求发布后 3 个工作日内**更新知识：

| 触发事件 | 需要更新的知识 |
|----------|----------------|
| 接口签名变更 | `applications/{app}/domain/base/api.md` + 引用该接口的 flow |
| 新增/修改状态 | 对应 `state-*.md` |
| 新增业务身份或差异化逻辑 | 对应 `solution/` 目录 |
| 全局规则变更 | `main/rules/` |
| 全局技术约束变更 | `main/tech/` |
| 应用职责调整 | `application-{app}.md` |

### 10.2 更新操作

1. 更新正文内容
2. `version` +1（如涉及语义变更）
3. 更新 `updatedAt`
4. 如与真实来源核对，更新 `verifiedAt`
5. 更新 `evidence` 中的代码路径或文档链接
6. 在文件末尾的"变更历史"表格中追加记录

### 10.3 过时知识处理

- 发现知识与当前代码不一致时，首先标记 `status: DEPRECATED`
- `version +1`，`updatedAt` 更新
- 在文件顶部添加 `> ⚠️ 本文档已废弃，请勿作为事实引用` 的醒目提示
- 后续由 owner 决定是否重写（新建 DRAFT）或直接删除（极端情况）

---

## 十一、敏感信息与数据边界

> 原文强调："只让 Agent 读取当前需求需要的仓库和知识目录；敏感文档、线上数据、密钥、客户信息不进入 prompt。"

### 11.1 禁止进入知识库的内容

| 禁止内容 | 原因 |
|----------|------|
| 密钥、Token、数据库连接串 | 安全风险 |
| 生产环境敏感数据（用户手机号、身份证号等） | 隐私合规 |
| 客户信息、商家数据 | 数据合规 |
| 内部未公开的财务/资损数据 | 保密要求 |
| 未脱敏的线上日志（含真实用户数据） | 隐私合规 |

### 11.2 脱敏规范

- 知识库中所有示例、代码片段、日志片段**必须脱敏**
- **对外分享**必须脱敏应用名、类名、字段名、配置 key
- **跨团队分享**依据数据权限和信息密级处理，不强制全部脱敏
- 内部链接（如需求链接、Wiki 链接）在知识库中保留，但 AI 读取时应注意权限控制

---

## 十二、confidence 与 stability 的维护策略

`confidence` 和 `stability` 不是装饰字段，必须真正影响维护策略：

| stability | 维护策略 |
|-----------|----------|
| `stable` | 可作为稳定上下文使用，无需每次回代码确认 |
| `evolving` | 优先核对，编码前建议回代码确认 |
| `volatile` | AI 每次编码**必须**回代码确认，知识库仅作为定位入口 |

| confidence | 使用策略 |
|------------|----------|
| `high` | 可直接引用 |
| `medium` | 引用时建议交叉验证 |
| `low` | 仅作为线索，必须回到代码或人工确认 |

---

## 十三、违规处理

| 违规情况 | 处理方式 |
|----------|----------|
| AI 写入了不符合模板结构的知识 | 人工在 review 时要求修正，或 AI 自动回滚 |
| AI 将 CANDIDATE 内容直接引用为事实 | 在 validate 阶段拦截，要求回到代码核对 |
| 发现 OFFICIAL 知识但实际已过期 | 立即标记 DEPRECATED，通知 owner 更新 |
| 有人绕过了 candidate 直接写 OFFICIAL | 团队 review 时指出，补充 evidence 和 owner 确认 |

---

## 附录：AI 使用指引（给 Coding Agent 看的）

> 当你需要使用或写入知识库时，请遵守以下流程：
>
> **首次接触知识库时**：
> 1. 读取本文件（`KNOWLEDGE-RULES.md`），理解全局规则
>
> **每个具体需求**：
> 1. 读取 `ROUTING.md`，根据需求定位到候选知识文件
> 2. 按路由结果读取目标知识文件
> 3. **编码前，回到当前仓库核对代码**——知识库只提供定位入口和稳定上下文
>
> **写入新知识时**：
> 1. 先确定 `type`，找到 `template/` 下对应模板
> 2. 套用模板，填写完整的 Front Matter（含本文件定义的所有公共字段）
> 3. 根据内容归属判定，放入正确的目录
> 4. 如果是新发现的知识，先放 `candidate/`，状态设为 `DRAFT` 或 `CANDIDATE`