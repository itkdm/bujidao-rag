---
id: KB-INFRA-GLOBAL-METADATA-RULES
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- knowledge-base
- governance
- front-matter
anchors:
- GLOBAL:METADATA-RULES
---

# 知识库元数据字段规范

> 本文件是 `knowledge/` 的元数据字段规范文件。
---

## 一、Front Matter 设计原则

Front Matter 是知识库的结构化元数据层，主要服务于：

- 脚本统一校验与维护
- AI Agent / Skill 自动读取和写入
- 文档检索、分类和统计
- 生命周期管理
- 应用归属统计
- 知识可信度判断
- 后续批量迁移和自动化治理

字段分为三类：

### 1. 全局字段

所有受知识库管理的 Markdown 文件统一使用。

### 2. 知识字段

仅真正承载知识内容的文件使用。

### 3. 类型专属字段

仅特定 `type` 确有机器管理需求时增加。

类型专属字段不在本版统一定义，后续按实际需求逐类补充。

---

# 二、字段总览

## 2.1 全局必填字段（10)

所有受管理文件统一包含：

```yaml
id:
scope:
status:
owner:
maintainers:
version:
updatedAt:
verifiedAt:
tags:
anchors:
```

---

## 2.2 全局条件字段(1)

```yaml
appCode:
```

`appCode` 是否出现由 `scope` 决定。

---

## 2.3 知识文件必填字段(4)

真正承载知识内容的文件，在全局字段基础上增加：

```yaml
type:
confidence:
stability:
evidence:
```

固定基础设施文件不强制使用这些知识字段。

---

# 三、全局字段规范

## 3.1 id

### 作用

`id` 是文件在知识库中的**永久唯一身份**。

### 格式

统一：

```text
KB-{CATEGORY}-{KEY}
```

例如：

```yaml
id: KB-INFRA-ROUTING
id: KB-RULE-GIT-COMMIT
id: KB-FEATURE-USER-MANAGEMENT
id: KB-TECH-SPRING-TRANSACTION
```

### CATEGORY

基础设施文件：

```text
INFRA
```

知识文件原则上使用对应 `type` 的规范化大写值。

例如：

```text
rule    → RULE
feature → FEATURE
tech    → TECH
```

### KEY

`KEY` 是稳定的语义标识。

规则：

- 仅允许 `A-Z`、`0-9`、`-`
- 必须全大写
- 多个单词使用 `-`
- 不使用中文
- 不使用空格或 `_`

正确：

```text
GIT-COMMIT
USER-MANAGEMENT
SPRING-TRANSACTION
```

### 唯一性

`id` 必须在整个 `knowledge/` 范围内全局唯一。

### 稳定性

`id` 创建后原则上不得修改。

以下变化均不应导致 `id` 改变：

- 文件重命名
- 文件移动
- `scope` 变化
- `appCode` 变化
- `owner` 变化
- `status` 变化
- 内容版本变化

只有 ID 重复、初始 ID 明显错误等特殊迁移场景才允许修改。

### appCode 与 id

`appCode` **不强制进入 `id`**。

只有发生全局 ID 重名时，才可以在 `KEY` 中加入稳定的区分信息。

---

## 3.2 scope

### 作用

`scope` 表示内容的**适用范围**，不表示文件归属于哪个应用。

### 系统封闭枚举

只允许：

```text
global
app
cross-app
```

含义：

| 值 | 含义 |
|---|---|
| `global` | 整个知识库 / 团队全局适用 |
| `app` | 仅适用于单一应用 |
| `cross-app` | 同时涉及多个应用，但不是全局规则 |

这三个值属于**系统封闭枚举**，项目初始化时不得增加、删除或修改。

---

## 3.3 appCode

### 作用

`appCode` 表示文档主要归属的**单一应用机器标识**。

主要用于：

- 按应用统计知识数量
- 应用级筛选
- Skill 自动管理
- 路径与 Front Matter 一致性校验

### 条件规则

#### scope: app

必须填写：

```yaml
scope: app
appCode: ruoyi-vue-pro
```

#### scope: global

禁止填写 `appCode`。

#### scope: cross-app

禁止填写单一 `appCode`。

如果未来确实需要描述多个应用，需单独设计，不在本版扩展 `appCode` 语义。

### 格式

`appCode`：

- string
- 全小写
- 使用 kebab-case
- 仅允许 `a-z`、`0-9`、`-`

例如：

```text
ruoyi-vue-pro
yudao-ui-admin-vue3
order-service
```

### 注册要求

`appCode` 属于**项目可扩展注册值**。

所有合法 `appCode` 必须先登记在本文的「项目可扩展注册区」。

禁止文档临时创造未注册的 `appCode`。

禁止使用：

```text
global
none
n/a
unknown
```

等占位值。

---

## 3.4 status

### 作用

`status` 只表示文件的生命周期状态。

### 系统封闭枚举

固定为：

```text
DRAFT
CANDIDATE
OFFICIAL
DEPRECATED
```

| 值 | 含义 |
|---|---|
| `DRAFT` | 正在编写，内容尚不完整 |
| `CANDIDATE` | 内容基本完整，等待确认 |
| `OFFICIAL` | 已确认，可作为正式内容使用 |
| `DEPRECATED` | 曾经有效，但当前已经过期或不再推荐 |

项目不得自行增加：

```text
REVIEWING
PUBLISHED
ARCHIVED
```

等新状态。

### 常规状态流转

允许：

```text
DRAFT → CANDIDATE
CANDIDATE → DRAFT
CANDIDATE → OFFICIAL
OFFICIAL → CANDIDATE
OFFICIAL → DEPRECATED
DEPRECATED → CANDIDATE
```

不使用：

```text
OFFICIAL → DRAFT
```

需要重新确认时退回 `CANDIDATE`。

---

## 3.5 owner

### 作用

`owner` 表示文件的**最终责任主体**。

它不表示：

- 谁创建了文件
- 谁最后编辑了文件
- 当前由谁执行维护工作

### 规则

- 必填
- string
- 只能有一个
- 可以是团队，也可以是个人
- 必须来自项目已注册的 owner 列表
- 只有最终责任归属真正变化时才修改

例如：

```yaml
owner: backend-platform
```

或：

```yaml
owner: bujidao
```

---

## 3.6 maintainers

### 作用

`maintainers` 表示当前实际负责维护、更新和核验该文件的人员。

### 规则

- 必填
- `list<string>`
- 至少 1 个
- 只能填写具体用户
- 必须来自项目已注册的用户列表
- 即使与 `owner` 相同，也不能省略

例如：

```yaml
owner: bujidao
maintainers:
- bujidao
```

或者：

```yaml
owner: backend-platform
maintainers:
- zhangsan
- lisi
```

禁止简写为：

```yaml
maintainers: zhangsan
```

---

## 3.7 version

### 作用

`version` 表示当前文件的**语义版本号**。

### 格式

```yaml
version: 1
```

规则：

- integer
- 最小值为 `1`
- 新文件从 `1` 开始
- 只增不减
- 不允许复用历史版本号

### 需要 +1

发生语义变化时：

- 正文含义变化
- `scope` 变化
- `appCode` 变化
- `status` 变化
- `owner` / `maintainers` 变化
- `tags` / `anchors` 实质变化
- `type` 变化
- `confidence` / `stability` 变化
- `evidence` 实质变化

统一：

```text
version +1
```

包括：

```text
OFFICIAL → DEPRECATED
```

### 不需要 +1

纯非语义修改：

- 错别字
- 空格
- 换行
- Markdown 排版
- 标点
- 不改变身份的文件重命名
- 不改变知识语义的目录移动
- 仅重新验证并更新 `verifiedAt`

---

## 3.8 updatedAt

### 作用

表示文件最后一次发生修改的日期。

格式固定：

```yaml
updatedAt: YYYY-MM-DD
```

例如：

```yaml
updatedAt: 2026-08-18
```

任何文件修改都必须更新 `updatedAt`，包括：

- 正文
- Front Matter
- 格式
- 错别字

不记录具体时分秒，精确提交时间由 Git 管理。

---

## 3.9 verifiedAt

### 作用

表示文件内容最后一次被确认仍然正确、有效的日期。

格式：

```yaml
verifiedAt: YYYY-MM-DD
```

### 核心规则

普通编辑：

```text
更新 updatedAt
不自动更新 verifiedAt
```

只有实际重新核对了真实来源、当前代码、正式文档或负责人确认后，才更新 `verifiedAt`。

必须满足：

```text
verifiedAt <= updatedAt
```

重新验证但内容无需修改时，可以只更新 `verifiedAt`，此操作不要求 `version +1`。

---

## 3.10 tags

### 作用

用于：

- 宽泛检索
- 分类
- 统计
- RAG 召回

### 规则

- 必填
- `list<string>`
- 至少 1 个
- 允许多个
- 值开放，不要求提前注册

格式：

- 全小写
- kebab-case
- 仅允许 `a-z`、`0-9`、`-`

例如：

```yaml
tags:
- git
- code-review
- spring-boot
```

禁止同一概念使用多种不同格式。

---

## 3.11 anchors

### 作用

`anchors` 用于机器路由、精确关联和稳定匹配。

它与 `tags` 的职责不同：

```text
tags    → 宽泛搜索
anchors → 精确机器语义
id      → 唯一身份
```

### 格式

```text
{NAMESPACE}:{VALUE}
```

例如：

```yaml
anchors:
- GLOBAL:GIT-COMMIT
- APP:RUOYI-VUE-PRO
- FEATURE:USER-MANAGEMENT
```

规则：

- 必填
- `list<string>`
- 至少 1 个
- `NAMESPACE` 全大写
- `VALUE` 全大写
- 多词使用 `-`

### 唯一性

anchor 不要求全局唯一。

多个文件可以共享：

```text
APP:RUOYI-VUE-PRO
```

真正承担全局唯一身份的是 `id`。

### Namespace

Anchor Namespace 使用：

> 系统内置值 + 项目注册扩展值

内置值见「项目可扩展注册区」。

未注册 Namespace 不允许直接使用。

---

# 四、知识文件字段规范

以下字段只用于真正承载知识内容的文件。

固定基础设施文件不要求填写。

---

## 4.1 type

### 作用

`type` 表示知识内容的结构类别。

它不表示：

- 文件所在目录
- 业务领域
- 生命周期状态
- 应用归属

### 格式

- string
- 全小写
- kebab-case
- 仅允许 `a-z`、`0-9`、`-`

### 合法值

合法 `type`：

```text
系统内置 type
+
项目注册 custom type
```

未注册的值禁止使用。

### 内置 type

当前固定：

```text
application
feature
rule
tech
base
flow
state
glossary
```

项目可以扩展新的 type，但必须先在「项目可扩展注册区」登记。

新增 type 前，应先确认现有 type 无法合理表达该知识。

---

## 4.2 confidence

### 作用

表示：

> 我们有多确定这份知识**当前是正确的**。

### 系统封闭枚举

固定：

```text
high
medium
low
```

| 值 | 含义 |
|---|---|
| `high` | 有明确强证据，可以较高信任 |
| `medium` | 有一定依据，但仍存在未完全确认的信息 |
| `low` | 主要依赖推断或证据不足 |

`confidence` 不允许项目自定义扩展。

### Agent 使用规则

```text
low
→ 不应直接作为最终事实，必须继续核验

medium
→ 可以作为辅助上下文，关键结论应再次确认

high
→ 可以正常使用，但仍需结合 stability 和 verifiedAt 判断
```

---

## 4.3 stability

### 作用

表示：

> 即使这份知识当前正确，它未来有多容易发生变化。

### 系统封闭枚举

固定：

```text
stable
evolving
volatile
```

| 值 | 含义 |
|---|---|
| `stable` | 长期相对稳定 |
| `evolving` | 正在持续演进，可能随着需求或版本调整 |
| `volatile` | 很容易变化，使用前应重新核对真实来源 |

`stability` 不允许项目自定义扩展。

### Agent 使用规则

```text
volatile
→ 执行相关修改前必须重新核对真实来源

evolving
→ 涉及实际修改时优先重新核验

stable
→ 可以作为稳定上下文使用
```

### 与 confidence 的关系

两者完全独立。

例如：

```yaml
confidence: high
stability: volatile
```

表示：

> 当前非常确定是正确的，但未来非常容易变化。

---

## 4.4 evidence

### 作用

表示支撑该知识成立的证据来源。

### 结构

必须使用：

```yaml
evidence:
- type: code
  ref: path/to/code
- type: doc
  ref: path/or/url
- type: human
  ref: user-code
```

规则：

- 必填
- `list<object>`
- 至少 1 条
- 每条必须包含 `type`
- 每条必须包含 `ref`
- 允许同一种 type 出现多次

禁止：

```yaml
evidence:
- "OrderService.java"
```

### evidence.type

属于**系统封闭枚举**。

固定：

```text
code
doc
human
```

不允许项目初始化时自行扩展。

#### code

来自当前代码、配置、迁移脚本等实现事实。

`ref` 必须尽可能精确、可定位。

#### doc

来自正式文档、RFC、ADR、需求文档、官方文档、内部文档等。

`ref` 必须能定位到具体文档。

#### human

来自明确人员确认。

`ref` 应使用可追溯的人员标识。

### evidence 与 confidence

`confidence` 必须结合 evidence 判断。

证据数量不等于证据质量，不允许通过简单统计 evidence 数量自动确定 `confidence`。

---

# 五、系统固定值与项目可扩展值

所有字段必须明确属于以下三类之一。

## 5.1 系统封闭值

这些值属于知识库协议本身。

后续开发者或Agent初始化项目时**禁止修改**。

### scope

```text
global
app
cross-app
```

### status

```text
DRAFT
CANDIDATE
OFFICIAL
DEPRECATED
```

### confidence

```text
high
medium
low
```

### stability

```text
stable
evolving
volatile
```

### evidence.type

```text
code
doc
human
```

---

## 5.2 系统内置 + 项目扩展值

系统提供基础值，项目初始化时允许追加，但不得随意修改系统内置值。

包括：

```text
type
anchor namespace
```

---

## 5.3 项目注册值

完全取决于当前项目或工作区，由 Agent 自动发现、确认并维护。

包括：

```text
appCode
owner
maintainers/user
```

这些值不得直接写死在知识库通用规则逻辑中，需由Agent自行判断或询问用户。

---

## 5.4 开放但格式受控

无需提前注册，但必须遵守格式规范。

包括：

```text
id
tags
anchor value
evidence.ref
```

---

# 六、项目可扩展注册区

> **本节是 Agent / 初始化脚本维护项目级可扩展值的固定区域。**
>
> 初始化或同步项目时，只修改本节对应注册项。
>
> 不得为了适配项目而修改前文定义的系统封闭枚举。

---

## 6.1 AppCode Registry

<!-- KB-REGISTRY:APP-CODE:BEGIN -->

```yaml
appCodes:
- ruoyi-vue-pro
- yudao-ui-admin-vue3
```

<!-- KB-REGISTRY:APP-CODE:END -->

规则：

- Agent 初始化时，必须先根据当前实际工作区识别应用
- 新应用必须先注册，再允许知识文件引用
- 已注册 appCode 应保持长期稳定

---

## 6.2 Custom Type Registry

系统内置：

```yaml
builtInTypes:
- application
- feature
- rule
- tech
- base
- flow
- state
- glossary
```

项目扩展区：

<!-- KB-REGISTRY:CUSTOM-TYPE:BEGIN -->

```yaml
customTypes: []
```

<!-- KB-REGISTRY:CUSTOM-TYPE:END -->

Agent 只能向 `customTypes` 追加经过确认的新类型，不得修改 `builtInTypes`。

---

## 6.3 Owner Registry

<!-- KB-REGISTRY:OWNER:BEGIN -->

```yaml
owners:
- bujidao
- backend-platform
```

<!-- KB-REGISTRY:OWNER:END -->

`owner` 可以注册：

- 团队 Code
- 用户 Code

---

## 6.4 User Registry

<!-- KB-REGISTRY:USER:BEGIN -->

```yaml
users:
- bujidao
```

<!-- KB-REGISTRY:USER:END -->

`maintainers` 中的所有值必须来自此注册表。

---

## 6.5 Anchor Namespace Registry

系统内置：

```yaml
builtInAnchorNamespaces:
- GLOBAL
- APP
- FEATURE
- RULE
- TECH
- BASE
- FLOW
- STATE
```

项目扩展区：

<!-- KB-REGISTRY:ANCHOR-NAMESPACE:BEGIN -->

```yaml
customAnchorNamespaces: []
```

<!-- KB-REGISTRY:ANCHOR-NAMESPACE:END -->

Skill 可以根据项目实际需要增加 Namespace，但必须先注册再使用。

---

# 七、标准 Front Matter

## 7.1 基础设施文件

```yaml
---
id: KB-INFRA-{KEY}
scope: global
status: OFFICIAL
owner: {registered-owner}
maintainers:
- {registered-user}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
tags:
- infrastructure
anchors:
- GLOBAL:{KEY}
---
```

---

## 7.2 单应用知识文件

```yaml
---
id: KB-{CATEGORY}-{KEY}
type: {registered-type}
scope: app
appCode: {registered-app-code}
status: DRAFT
owner: {registered-owner}
maintainers:
- {registered-user}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
confidence: low
stability: evolving
evidence:
- type: code
  ref: {traceable-reference}
tags:
- {tag}
anchors:
- APP:{APP-CODE}
---
```

---

## 7.3 全局知识文件

```yaml
---
id: KB-{CATEGORY}-{KEY}
type: {registered-type}
scope: global
status: DRAFT
owner: {registered-owner}
maintainers:
- {registered-user}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
confidence: low
stability: evolving
evidence:
- type: doc
  ref: {traceable-reference}
tags:
- {tag}
anchors:
- GLOBAL:{KEY}
---
```

---

## 7.4 跨应用知识文件

```yaml
---
id: KB-{CATEGORY}-{KEY}
type: {registered-type}
scope: cross-app
status: DRAFT
owner: {registered-owner}
maintainers:
- {registered-user}
version: 1
updatedAt: YYYY-MM-DD
verifiedAt: YYYY-MM-DD
confidence: low
stability: evolving
evidence:
- type: doc
  ref: {traceable-reference}
tags:
- {tag}
anchors:
- {NAMESPACE}:{VALUE}
---
```

`scope: cross-app` 不填写单一 `appCode`。