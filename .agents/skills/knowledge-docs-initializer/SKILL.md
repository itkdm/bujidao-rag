---
name: knowledge-docs-initializer
description: 根据当前工作区可验证的项目事实，初始化或调整 knowledge/ 知识库与 docs/ 研发文档体系。适用于项目启动、接入模板，或需要重新识别应用边界、技术栈版本、芋道形态和启用模块的场景；不负责实现产品功能，也不编造项目知识。
---

# 知识库与研发文档初始化

把仓库中的通用知识库与研发文档框架，初始化成符合当前工作区真实情况、可验证、可持续维护的项目实例。

仓库自带的芋道应用知识只是现成示例，不是目标项目的默认身份。目标项目可能采用不同芋道版本、不同模块或前端，也可能完全不使用芋道。

## 必读资料

修改文件前，必须完整阅读 [references/initialization-contract.md](references/initialization-contract.md)。它规定了哪些内容需要保留、重建、移除和验证。

如果工作区正在使用或可能使用芋道，还必须完整阅读 [references/yudao-variants.md](references/yudao-variants.md)，再判断应用边界和模块状态。

## 适用范围

本 Skill 可以初始化或调整：

- `knowledge/` 的基础设施、注册表、路由、索引和应用知识
- `docs/changes/` 与 `docs/postmortem/` 的基础设施和模板
- 从当前代码或用户明确确认中得到的项目知识

除非用户另行明确要求，否则不得修改产品代码、启用应用模块、变更依赖或创建实现决策。

## 工作流程

### 1. 确认来源与目标

确认工作区根目录并检查 `git status`，判断当前属于：

- 模板的新副本
- 正在接入知识体系的已有项目
- 需要重新校准的既有知识库

已有的人工 Change、Postmortem 和知识文件属于项目数据。不能仅因其与模板示例不同就覆盖或删除。

### 2. 识别真实项目

检查构建清单、包清单、启动入口、部署单元、配置文件和实际目录，形成有证据的应用清单。

每个候选应用至少识别：

- 稳定的 appCode
- 可独立构建、运行或部署的边界
- 语言、框架和版本
- 启动或运行入口
- 当前模块状态
- 与其他应用的真实关系

必须区分代码已验证事实、用户确认事实和未解决推断。会实质改变目录结构的未决问题应询问用户；其他推断只能进入 `candidate/`。

owner 与 maintainer 是特殊阻断项：它们不能从代码作者或 Git 提交人安全推断。如果目标责任人尚未明确注册并确认，先询问用户，并暂停生成受管理知识文件。

### 3. 制定初始化矩阵

编辑前明确“保留 / 重建 / 移除”矩阵：

- 保留通用基础设施和已确认的目标项目内容
- 根据目标工作区重建应用知识和注册表
- 只有确认属于模板且与目标无关时，才移除自带示例
- 归属不清的用户内容先保留，直到责任边界明确

删除 appCode、owner 或 maintainer 注册项前，必须搜索所有拟保留文件中的引用。只要仍有内容引用，就保留该注册值，直到相关内容经确认完成迁移、归档或删除。

未经验证，不得把示例 `applications/` 目录、appCode、owner、版本、模块或证据路径复制到目标项目。

### 4. 初始化 knowledge

遵守 `knowledge/KNOWLEDGE-METADATA-RULES.md`，并使用 `knowledge/template/` 下的模板。

每个应用必须实例化以下四个配方，并替换全部占位符：

- `application-README-template.md`
- `application-INDEX-template.md`
- `application-overview-template.md`
- `category-INDEX-template.md`

分类 README 只复用正文职责契约，必须丢弃模板基础设施 Front Matter。任何模板 Front Matter 都不能原样复制到目标应用；目标文件的 ID、scope、appCode、owner、maintainers、日期、tags 和 anchors 必须根据目标注册表与真实上下文生成。

- 注册当前应用，以及仍被历史归档引用的稳定 appCode；注册已确认的 owner 和 maintainers。
- 将所有保留的受管理基础设施文件重新绑定到目标 owner/maintainers，并按元数据规则更新 `version` 与 `updatedAt`。
- 每个真实应用边界建立一个应用知识目录。
- 应用总览只能使用当前证据生成。
- `base/`、`feature/`、`rule/`、`tech/` 只写已确认知识。
- 推断或未决结论放入 `candidate/`。
- 外部资料保留在 `reference/`，不得自动提升为项目事实。
- 重新生成所有受影响的 INDEX，并按真实文件系统更新 ROUTING。

Agent 新生成的项目知识保持 `DRAFT` 或 `CANDIDATE`，未经 owner review 不得直接晋升为 `OFFICIAL`。

### 5. 初始化 docs

保持 Change 与 Postmortem 框架业务中立，并保留生命周期目录、README 和模板。

不得虚构初始 Change 或 Postmortem。只有初始化本身确实包含符合触发条件的设计取舍、行为变化或真实事故时，才创建相应记录。

### 6. 验证

运行仓库校验并检查完整差异：

```text
python knowledge/scripts/validate_metadata.py
python knowledge/scripts/metadata_report.py
python .agents/skills/knowledge-docs-initializer/scripts/validate_initialization.py .
git status --short
git ls-files --others --exclude-standard
git diff --check
```

结构校验器会检查目录骨架、本地 Markdown 链接、证据路径、注册表与目录关系、INDEX 完整性，以及实例化应用、Change 和 Postmortem 中的未完成占位符。模板目录和通用基础设施可以保留契约明确规定的路径元变量，不能把它们当作初始化残留清理。

必须同时检查 Git 列出的 tracked 和 untracked 文件；单独执行 `git diff` 无法覆盖新生成文件。

### 7. 交付说明

最终报告至少包含：

- 项目形态，以及当前应用与退休应用清单
- 保留、重建、移除和暂存的内容
- 证据来源与未解决问题
- 验证结果
- 需要 owner review 后才能转为正式状态的文件

除非用户同时要求修改应用代码，否则知识库和 docs 初始化完成后停止。

## 不可违反的边界

- 不得让目标项目继承模板中的产品、行业、功能集合或芋道模块选择。
- 不得把上游模块、目录、依赖或参考资料当成目标项目实际采用的证据。
- 不得把未经确认的 Agent 推断直接写入 `main/` 或 `applications/`。
- 不得在缺乏证据和明确范围时覆盖用户已有项目记录。
- 不得在实例化的 application、Change 或 Postmortem 中留下断链、失效 appCode 或未解析模板占位符。
