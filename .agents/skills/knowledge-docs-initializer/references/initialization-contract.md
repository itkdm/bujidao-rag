# 初始化契约

本文件定义 `knowledge/` 与 `docs/` 从模板形态变成目标项目实例时必须遵守的保留、重建和验证规则。执行初始化前完整读取。

## 1. 预期结果

```text
<workspace>/
├── AGENTS.md
├── knowledge/
│   ├── README.md
│   ├── INDEX.md
│   ├── ROUTING.md
│   ├── main/
│   ├── applications/
│   │   └── <从目标工作区识别出的 appCode>/
│   │       ├── README.md
│   │       ├── INDEX.md
│   │       ├── <appCode>.md
│   │       ├── base/README.md + INDEX.md
│   │       ├── feature/README.md + INDEX.md
│   │       ├── rule/README.md + INDEX.md
│   │       └── tech/README.md + INDEX.md
│   ├── candidate/
│   │   ├── main/
│   │   └── applications/
│   ├── personal/
│   │   └── <存在真实个人内容时建立的 ownerCode>/
│   ├── archive/
│   │   ├── main/
│   │   ├── applications/
│   │   ├── candidate/
│   │   ├── personal/
│   │   ├── reference/
│   │   └── template/
│   ├── reference/
│   │   ├── README.md
│   │   └── INDEX.md
│   ├── template/
│   │   ├── README.md
│   │   ├── INDEX.md
│   │   ├── common/
│   │   ├── candidate/
│   │   ├── personal/
│   │   │   └── {ownerCode}/
│   │   └── applications/
│   └── scripts/
│       ├── README.md
│       ├── validate.py
│       ├── validate_candidate.py
│       └── validate_personal.py
└── docs/
    ├── changes/
    │   ├── README.md
    │   ├── proposed/
    │   ├── implemented/
    │   ├── rejected/
    │   ├── archived/
    │   └── templates/
    └── postmortem/
        ├── README.md
        └── templates/
```

空目录不靠虚构知识填充。没有正式 feature、rule 或 tech 时，只保留其 README 与 INDEX。

根级 `AGENTS.md` 是自动加载入口，不是完整知识或研发文档的副本。

`knowledge/scripts/` 是初始化结果的自包含校验器，不依赖 `.agent/`、`.agents/` 或 Skill 安装位置。Skill 本身可按宿主约定放在 `.agent/skills/` 或 `.agents/skills/`；本契约不要求初始化完成后保留某一种宿主目录名称。

## 2. 内容分类

| 类别 | 处理方式 | 典型内容 |
| --- | --- | --- |
| 通用基础设施 | 保留并按目标项目调整 | 目录契约、路由、索引、通用模板 |
| 上游示例 | 仅在与目标项目匹配时作为证据 | 芋道应用知识、芋道官方参考资料 |
| 目标项目现有内容 | 保留并核对，禁止无依据覆盖 | 已有知识、Change、Postmortem、人工决策 |
| 无关示例或失效内容 | 确认属于模板样例时移除 | 不存在的应用、无关技术栈、失效引用 |

显式“初始化此模板到当前项目”的请求允许重建模板自带的示例应用目录，但不自动授权删除无法确认来源的用户文档。

## 3. 事实来源和可信度

按以下优先级建立项目事实：

1. 当前代码、构建清单、入口文件和运行配置。
2. 当前仓库已确认的 Change、项目规范和架构文档。
3. 用户在本次初始化中明确确认的信息。
4. 上游官方文档，只用于解释上游能力或版本。
5. 推断，只能进入 `candidate/` 或明确标记待确认。

不要把目录名、依赖存在、上游模块存在或参考资料存在直接解释为功能已启用。

## 4. 初始化清单

### 4.1 项目边界

至少识别仓库根目录和工作树状态、应用边界、构建与运行入口、语言与框架、调用关系、模块启用情况及基础设施入口。

只把有稳定边界的应用建立为 `applications/<appCode>/`。appCode 使用小写 kebab-case；普通源码包、共享目录或未启用模块不自动成为应用。

### 4.2 应用知识

为每个 appCode 从 `knowledge/template/applications/{appCode}/` 建立固定目录：

- `application-README-template.md` → `applications/<appCode>/README.md`
- `application-INDEX-template.md` → `applications/<appCode>/INDEX.md`
- `application-overview-template.md` → `applications/<appCode>/<appCode>.md`
- `category-INDEX-template.md` → 四类目录的 `INDEX.md`
- 四个分类目录的 `README.md` → 对应目标分类职责说明

模板是普通 Markdown 配方，`{{初始化:字段}}` 是必须替换的高识别度标记。目标文件不添加自定义 YAML Front Matter；应用身份和知识类别由目录及文件名表达。必须替换全部初始化标记。应用总览及 base、feature、rule、tech 正式知识统一使用 `## 证据来源` 下的 `code/doc` 表格，本地代码与文档来源使用工作区内可校验的 Markdown 链接。

应用总览至少记录应用边界、版本与技术栈、构建或运行入口、已启用模块、应用关系和使用前应复核的易变事实。

应用身份必须四处一致：目录名为 `applications/<appCode>/`，总览文件名为 `<appCode>.md`，总览“应用编码”值等于 appCode，README 声明同一应用边界，INDEX 链接同名总览。

### 4.3 四类知识边界

| 目录 | 只回答 |
| --- | --- |
| `base/` | 当前事实是什么，代码或资源在哪里 |
| `feature/` | 当前已经实现并可观察的能力是什么 |
| `rule/` | 当前项目必须满足什么约束 |
| `tech/` | 当前应用实际如何实现 |

规划中的功能不进入 `feature/`；未确认技术选型不进入正式 `tech/`；规则必须来自代码、现有决策或用户确认。

### 4.4 main、reference 与暂存区

- `main/` 只保留跨应用强制统一、已确认且长期有效的知识。
- `reference/` 是证据层，不是项目事实层；原始导入资料可以保留其上游来源追溯信息。
- `candidate/` 接收可能成为长期知识、但证据、范围或确认条件尚未闭环的结论；它不是草稿箱、资料库或任务列表。
- `personal/` 不作为团队正式结论，并按稳定 ownerCode 隔离不同所有者的内容。
- `archive/` 只保存已确认退出当前有效知识路径的内容，并按来源内容域保留原相对路径。

### 4.5 候选知识

`candidate/` 使用目标镜像而不是状态目录：

- `candidate/main/<relative-path>` 拟晋升到 `main/<relative-path>`。
- `candidate/applications/<appCode>/<relative-path>` 拟晋升到 `applications/<appCode>/<relative-path>`。
- candidate 中的 appCode 必须已经存在于正式 applications；应用边界尚未确认时进入 unclassified。
- 只有目标范围也无法判断时才按需建立 `candidate/unclassified/`，完成分类后必须迁出。
- 文件名使用未来正式知识的文件名，不添加 candidate 前缀；每个子目录继续使用 README + INDEX 协议。
- 每级 `README.md` 与 `INDEX.md` 是保留的导航基础设施，不是候选正文，不参与目标镜像和晋升；候选知识不得使用这两个文件名。
- 候选正文从 `template/candidate/candidate.md` 实例化，必须写明候选结论、唯一拟晋升位置、仍为候选的原因、证据、待确认问题和验证与晋升条件。
- 不使用百分比可信度，不建立 pending、reviewed、approved 等状态目录。确认后的内容必须退出 candidate。
- 外部资料进入 reference，个人素材进入 personal，待实施方案进入 `docs/changes/proposed/`，普通 TODO 进入任务系统。
- 正式文档中的局部复核提醒可以保留；形成独立假设、独立证据或跨文件影响时才抽成候选。
- 目标文件不存在时可用 `git mv` 晋升并重写为正式结构；目标已存在时合入已验证内容，禁止覆盖正式知识。

### 4.6 个人知识

- 个人内容只能写入 `personal/<ownerCode>/`，不能直接放在 personal 根目录。
- ownerCode 是当前仓库内唯一且长期不变的小写 kebab-case 标识；姓名、昵称和团队称呼只作为所有者 README 中的显示信息。
- ownerCode 由仓库分配，冲突时使用稳定后缀；不得直接使用邮箱、手机号、工号等敏感或组织绑定信息。
- 只有产生真实个人内容时才从 `template/personal/{ownerCode}/` 实例化目录，不为登记人员预造空目录。
- 每个所有者目录及其主题子目录继续使用 README + INDEX 协议，并至少包含一份非导航的个人 Markdown 内容。
- personal 不强制建立 main、applications 或知识类型镜像；个人素材形成独立候选结论后，再按 candidate 契约确定拟晋升路径。
- ownerCode 目录只隔离来源归属，不提供访问控制或隐私隔离。personal 内容进入共享版本库并可能被自动化工具读取；不得存放密码、Token、私密通信、个人隐私或其他不应进入仓库的信息。
- 归档时保留 ownerCode 和 personal 内原相对路径，映射到 `archive/personal/<ownerCode>/<relative-path>`。

### 4.7 归档镜像

`archive/` 是知识内容目录的微缩镜像，只允许六个根目录：`main/`、`applications/`、`candidate/`、`personal/`、`reference/`、`template/`。

- `knowledge/<content-root>/<relative-path>` 归档到 `knowledge/archive/<content-root>/<relative-path>`。
- 不镜像 `archive/` 自身，也不把 `docs/`、根级导航或校验脚本作为普通知识归档。
- 六个来源内容域根部的 `README.md` 与 `INDEX.md` 是导航基础设施，只在原位更新并由 Git 保留历史，不归档到已占用的同名路径。
- 对已跟踪文件使用 `git mv`；归档后更新来源和目标 INDEX、默认 ROUTING 及所有相关相对链接。
- 标准归档路径冲突时，先在同一镜像树内重命名既有归档历史，再把当前来源文件移动到标准映射路径，禁止覆盖历史。
- 原始导入资料根目录使用普通文件 `.raw-reference` 显式标记；标记只能放在 `reference/` 或 `archive/reference/` 的资料子目录根部，不能直接放在 reference 根部或使用符号链接。归档时必须连同标记、来源说明和本地资源整体移动。
- 新的 appCode、分类或参考资料子目录只在真实归档发生时创建。
- 禁止在 `knowledge/` 其他位置维护 `archive`、`archived`、`legacy`、`deprecated`、`obsolete` 等旁路归档目录。
- `knowledge/` 下不得使用目录符号链接或 Windows junction 绕过内容域与归档边界。

## 5. docs 初始化

`docs/changes/` 和 `docs/postmortem/` 是通用研发过程框架，不按目标业务预填内容。

- 保留 README、生命周期目录和模板。
- 保留目标项目已有的真实 Change 与 Postmortem。
- 不为目录完整而虚构 Change、Spec、Design、Plan 或 Postmortem。
- Change 的类型和状态由路径表达。
- Postmortem 只记录已经发生且满足触发条件的问题。

## 6. 索引和路由

- 根级 `AGENTS.md` 遵循 `knowledge/main/rules/AGENTSmd 全局规范.md`，从 `knowledge/template/common/AGENTS-template.md` 建立或增量更新；必须按项目事实维护项目概述、技术栈、目录与模块职责、运行与开发方式、验证策略、项目特有规则六个必选章节。
- AGENTS 的文档规范保留精简入口：首次接触指向 knowledge README，每个具体任务指向 ROUTING，并链接 Change 与 Postmortem 规范；不得用路由片段替代完整项目上下文。
- 完整分类、读取顺序、写入位置和生命周期只在 `knowledge/ROUTING.md` 维护；AGENTS 不复制完整路由图。
- AGENTS 只保留当前工作区已验证的项目事实、硬约束和必要命令；详细知识、规范正文和变更过程分别链接到 knowledge 与 docs。
- AGENTS、knowledge、docs 和模板不得包含密码、Token、API Key、私密通信、个人隐私、本机专属路径或本地连接凭据。
- `README.md` 描述稳定职责，不维护动态文件清单。
- `INDEX.md` 覆盖当前目录所有有效直接子项，且不索引自身。
- `ROUTING.md` 基于实际 appCode、真实入口和现有知识更新。
- 删除或替换示例应用后，同步清理根 INDEX、applications INDEX、路由和正文引用。
- 不保留指向不存在文件的本地 Markdown 链接。
- 移动或归档文件后，所有继续引用该内容的相对链接必须改到新路径或替代知识。

## 7. 验证

初始化完成后至少执行：

```text
python knowledge/scripts/validate.py
git status --short
git ls-files --others --exclude-standard
git diff --check
```

本次发生归档或恢复移动时，再运行 `python knowledge/scripts/validate.py --git-staged`。CI 或推送前流程使用 `python knowledge/scripts/validate.py --git-range <base>...<head>` 检查对应提交范围；不要求本地同时运行两种 Git 模式。

归档和恢复应先用 `git mv` 完成标准路径移动，再编辑正文。暂存区模式要求 `knowledge/` 没有未暂存或未跟踪改动；校验器不根据两条无关的 A+D 记录猜测移动意图。

同时检查：

- 受管理的 `knowledge/` 与 `docs/` Markdown 没有自定义 YAML Front Matter
- 根级 AGENTS 具有全局规范要求的六个必选章节、唯一的精简路由入口和有效链接，并且没有复制 `knowledge/ROUTING.md` 的完整总路由图
- 所有本地 Markdown 链接存在且不越出工作区
- 每个应用目录名称有效，目录骨架完整，目录名、总览文件、“应用编码”、README 与 INDEX 身份一致
- candidate 目标镜像完整，候选正文的拟晋升位置与真实相对路径一致
- personal 内容按稳定 ownerCode 隔离，所有者 README 与目录标识一致，且不存在空所有者或主题目录
- archive 六个镜像根目录完整，其他位置没有旁路归档目录
- 显式启用 Git 模式时，归档和恢复操作保持来源内容域与原相对路径，且没有以复制代替移动
- INDEX 与真实文件系统一致
- 实例化的应用、Change 与 Postmortem 没有模板占位符、旧项目名称、无关应用和无依据结论
- 模板目录只保留契约允许的占位符
- 已检查 tracked diff 与 untracked 新文件，且 `git diff --check` 通过

原始导入参考资料的上游来源头，以及 Skill 包自身格式要求的 YAML，不属于知识文档自定义字段，允许保留。`.raw-reference` 标记目录内部的链接不由通用 Markdown 校验器验证；其资源完整性由抓取清单或导入工具负责，受管理知识指向该目录的链接仍必须有效。

## 8. 初始化报告

最终交付说明项目形态和应用清单、保留/重建/移除/暂存内容、事实来源、未确认问题、验证结果及应优先审查的候选知识。
