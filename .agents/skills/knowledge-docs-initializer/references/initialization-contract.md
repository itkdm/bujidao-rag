# 初始化契约

本文件定义 `knowledge/` 与 `docs/` 从模板形态变成目标项目实例时必须遵守的保留、重建和验证规则。执行初始化前完整读取。

## 1. 预期结果

初始化后的目录应满足：

```text
knowledge/
├── README.md
├── INDEX.md
├── ROUTING.md
├── KNOWLEDGE-METADATA-RULES.md
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
├── template/
└── scripts/

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

初始化前把现有内容分成四类：

| 类别 | 处理方式 | 典型内容 |
| --- | --- | --- |
| 通用基础设施 | 保留并按目标项目注册表调整 | 元数据规范、目录契约、校验脚本、通用模板 |
| 上游示例 | 仅在与目标项目匹配时作为证据；不得继承为项目事实 | 芋道应用知识、芋道官方参考资料 |
| 目标项目现有内容 | 保留并核对，禁止无依据覆盖 | 已有知识文件、Change、Postmortem、人工决策 |
| 无关示例或失效内容 | 已确认属于模板样例时移除；归属不清时先请求确认 | 不存在的应用、无关技术栈、失效引用 |

显式“初始化此模板到当前项目”的请求允许重建模板自带的示例应用目录，但不自动授权删除无法确认来源的用户文档。

## 3. 事实来源和可信度

按以下优先级建立项目事实：

1. 当前代码、构建清单、入口文件和运行配置。
2. 当前仓库已确认的 Change、项目规范和架构文档。
3. 用户在本次初始化中明确确认的信息。
4. 上游官方文档，只用于解释上游能力或版本。
5. 推断，只能进入 `candidate/` 或标记待确认。

不要把目录名、依赖存在、上游模块存在或参考资料存在直接解释为功能已启用。

## 4. 初始化清单

### 4.1 项目边界

至少识别：

- 仓库根目录和工作树状态
- 单仓库、多应用仓库或多服务仓库
- 每个可独立构建、运行或部署的应用
- 应用入口、构建工具、语言和主要框架
- 应用之间的调用关系
- 当前启用模块与仅存在但未启用的模块
- 配置、数据库、缓存、MQ 等基础设施入口

只把有稳定边界的应用注册为 `appCode`。普通源码包、共享目录或未启用模块不自动注册成应用。

### 4.2 注册表

注册集合只在 `KNOWLEDGE-METADATA-RULES.md` 的项目可扩展注册区维护：

- `appCodes`：目标项目真实应用，使用小写 kebab-case
- `owners`：目标项目确认的团队或人员 Code
- `users`：真实维护人员 Code
- `customTypes`：只有现有内置类型确实无法表达且经过确认时才扩展

不得修改 `scope`、`status`、`confidence`、`stability` 等系统封闭枚举。

删除任何 appCode、owner 或 maintainer 注册值前，必须搜索全部拟保留的受管理文件。只要仍有保留内容引用该值，就先保留注册；迁移责任人、归档退休应用或清理注册项需要明确确认。appCode 注册表因此可以同时包含当前应用身份与仍被 `archive/` 引用的稳定历史身份。

注册表确定后，必须把所有保留的受管理基础设施文件（包括根 README/INDEX/ROUTING、元数据规范、`main/`、各级索引与 `knowledge/template/**`）的 `owner`、`maintainers` 重绑定到目标注册值，并按元数据规则更新 `version` 与 `updatedAt`。“注册集合只在注册区维护”不禁止更新这些文件自身的 Front Matter。

`owner` 和 `maintainers` 不能从代码作者、Git 提交人或模板默认值推断。如果目标值尚未由用户明确确认，必须先询问并暂停受管理知识文件生成；不能用 `unknown`、模板作者或临时占位值绕过校验。

### 4.3 应用知识

为每个 appCode 从 `knowledge/template/applications/{appCode}/` 建立固定目录契约，并创建应用总览。必须实例化以下配方：

- `application-README-template.md` → `applications/<appCode>/README.md`
- `application-INDEX-template.md` → `applications/<appCode>/INDEX.md`
- `application-overview-template.md` → `applications/<appCode>/<appCode>.md`
- `category-INDEX-template.md` → `base/INDEX.md`、`feature/INDEX.md`、`rule/INDEX.md`、`tech/INDEX.md`
- 四个分类目录下的 `README.md` → 对应目标分类 README 的正文职责契约

四个 `*-template.md` 文件中的 Front Matter 是目标输出配方，必须替换全部占位符后实例化，不能原样复制。四个分类目录现有 `README.md` 中固定的是正文职责契约；其 `id`、`owner`、`maintainers`、日期、tags 和 anchors 属于模板基础设施元数据，必须丢弃。所有目标应用文件都要用目标注册表和应用路径生成完整 Front Matter。

应用总览至少记录：

- 当前应用是什么，不是什么
- 当前版本、技术栈和构建入口
- 启动或部署入口
- 当前启用模块
- 与其他应用的真实关系
- 使用前必须重新核对的易变事实

知识文件状态规则：

- 复制且未改变语义的基础设施模板可保持 `OFFICIAL`
- Agent 新生成的项目知识默认使用 `DRAFT` 或 `CANDIDATE`
- 未经 owner review，不得把新项目知识直接晋升为 `OFFICIAL`
- `evidence` 必须指向目标项目真实来源，不得保留模板项目路径

### 4.4 四类知识边界

| 目录 | 只回答 |
| --- | --- |
| `base/` | 当前事实是什么，代码或资源在哪里 |
| `feature/` | 当前已经实现并可观察的能力是什么 |
| `rule/` | 当前项目必须满足什么约束 |
| `tech/` | 当前应用实际如何实现 |

规划中的功能不进入 `feature/`；未确认技术选型不进入正式 `tech/`；业务规则必须来自代码、现有决策或用户确认。

### 4.5 main、reference 与暂存区

- `main/` 只保留跨应用强制统一、已确认且长期有效的知识。
- `reference/` 是证据层，不是项目事实层。目标项目使用芋道时可保留完整芋道官方资料，但不得默认路由到未启用模块；非芋道项目应移除、替换或从默认路由中排除芋道专属参考。
- `candidate/` 接收初始化中的推断、缺口和待确认结论。
- `personal/` 不作为团队正式结论。
- `archive/` 只保存已确认退出当前有效知识路径的内容。

## 5. docs 初始化

`docs/changes/` 和 `docs/postmortem/` 是通用研发过程框架，不按目标业务预填内容。

- 保留 README、生命周期目录和模板。
- 保留目标项目已有的真实 Change 与 Postmortem。
- 不为“目录看起来完整”虚构 Change、Spec、Design、Plan 或 Postmortem。
- 初始化过程只有在存在真实设计取舍、行为变化或需长期回溯时，才创建 Change。
- Change 的类型和状态只由路径表达。
- Postmortem 只记录已经发生且满足触发条件的问题。

## 6. 索引和路由

- `README.md` 描述稳定职责，不维护动态文件清单。
- `INDEX.md` 必须覆盖当前目录所有有效直接子项，且不索引自身。
- `ROUTING.md` 必须基于实际 appCode、真实入口和现有知识更新。
- 删除或替换示例应用后，同步清理根 INDEX、applications INDEX、注册表、路由和证据引用。
- 不允许保留指向不存在文件的本地 Markdown 链接或 `evidence.ref`。

## 7. 验证

初始化完成后至少执行：

```text
python knowledge/scripts/validate_metadata.py
python knowledge/scripts/metadata_report.py
python .agents/skills/knowledge-docs-initializer/scripts/validate_initialization.py .
git status --short
git ls-files --others --exclude-standard
git diff --check
```

同时检查：

- 所有本地 Markdown 链接存在
- 所有本地 `evidence.ref` 存在，或明确是 URL / 人工证据
- appCode、owner、maintainer 都已注册
- `applications/` 中每个当前应用目录都已注册；没有当前目录的历史 appCode 必须仍被 `archive/` 引用
- INDEX 与真实文件系统一致
- 实例化的应用、Change 与 Postmortem 输出没有模板占位符、旧项目名称、无关应用和无依据结论；通用基础设施中明确定义的路径元变量不视为初始化残留
- `knowledge/template/**` 与 `docs/**/templates/**` 只保留模板契约允许的占位符，不把这些占位符当成初始化残留
- 已检查 Git 列出的 tracked diff 与 untracked 新文件，且 `git diff --check` 通过

若某项无法验证，最终报告必须明确说明，不得声称已经完成。

## 8. 初始化报告

最终交付至少说明：

- 识别出的项目形态，以及当前应用与退休应用清单
- 保留、重建、移除和暂存了什么
- 哪些事实来自代码，哪些来自用户确认
- 尚未确认的关键问题
- 验证命令及结果
- 建议 owner 优先审查的知识文件
