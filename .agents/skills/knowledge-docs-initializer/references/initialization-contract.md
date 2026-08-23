# 初始化契约

本文件定义 `knowledge/` 与 `docs/` 从模板形态变成目标项目实例时必须遵守的保留、重建和验证规则。执行初始化前完整读取。

## 1. 预期结果

```text
knowledge/
├── README.md
├── INDEX.md
├── ROUTING.md
├── main/
├── applications/
│   └── <从目标工作区识别出的 appCode>/
│       ├── README.md
│       ├── INDEX.md
│       ├── <appCode>.md
│       ├── base/README.md + INDEX.md
│       ├── feature/README.md + INDEX.md
│       ├── rule/README.md + INDEX.md
│       └── tech/README.md + INDEX.md
├── candidate/
├── personal/
├── archive/
├── reference/
└── template/

docs/
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
- `candidate/` 接收初始化中的推断、缺口和待确认结论。
- `personal/` 不作为团队正式结论。
- `archive/` 只保存已确认退出当前有效知识路径的内容。

## 5. docs 初始化

`docs/changes/` 和 `docs/postmortem/` 是通用研发过程框架，不按目标业务预填内容。

- 保留 README、生命周期目录和模板。
- 保留目标项目已有的真实 Change 与 Postmortem。
- 不为目录完整而虚构 Change、Spec、Design、Plan 或 Postmortem。
- Change 的类型和状态由路径表达。
- Postmortem 只记录已经发生且满足触发条件的问题。

## 6. 索引和路由

- `README.md` 描述稳定职责，不维护动态文件清单。
- `INDEX.md` 覆盖当前目录所有有效直接子项，且不索引自身。
- `ROUTING.md` 基于实际 appCode、真实入口和现有知识更新。
- 删除或替换示例应用后，同步清理根 INDEX、applications INDEX、路由和正文引用。
- 不保留指向不存在文件的本地 Markdown 链接。

## 7. 验证

初始化完成后至少执行：

```text
python .agents/skills/knowledge-docs-initializer/scripts/validate_initialization.py .
git status --short
git ls-files --others --exclude-standard
git diff --check
```

同时检查：

- 受管理的 `knowledge/` 与 `docs/` Markdown 没有自定义 YAML Front Matter
- 所有本地 Markdown 链接存在且不越出工作区
- 每个应用目录名称有效，目录骨架完整
- INDEX 与真实文件系统一致
- 实例化的应用、Change 与 Postmortem 没有模板占位符、旧项目名称、无关应用和无依据结论
- 模板目录只保留契约允许的占位符
- 已检查 tracked diff 与 untracked 新文件，且 `git diff --check` 通过

原始导入参考资料的上游来源头，以及 Skill 包自身格式要求的 YAML，不属于知识文档自定义字段，允许保留。

## 8. 初始化报告

最终交付说明项目形态和应用清单、保留/重建/移除/暂存内容、事实来源、未确认问题、验证结果及应优先审查的候选知识。
