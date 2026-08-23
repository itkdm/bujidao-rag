---
name: knowledge-docs-initializer
description: 根据当前工作区可验证的项目事实，初始化或调整 knowledge/ 知识库与 docs/ 研发文档体系。适用于项目启动、接入模板，或需要重新识别应用边界、技术栈版本、芋道形态和启用模块的场景；不负责实现产品功能，也不编造项目知识。
---

# 知识库与研发文档初始化

把本仓库的通用知识库与研发文档框架，初始化成符合目标工作区真实情况、可验证、可持续维护的项目实例。

仓库自带的芋道应用知识只是现成示例，不是目标项目的默认身份。目标项目可以采用不同芋道版本、不同模块或前端，也可以完全不使用芋道。

## 必读资料

修改文件前，必须完整阅读 [references/initialization-contract.md](references/initialization-contract.md)。

如果工作区正在使用或可能使用芋道，还必须完整阅读 [references/yudao-variants.md](references/yudao-variants.md)，再判断应用边界和模块状态。

## 适用范围

本 Skill 可以初始化或调整：

- `knowledge/` 的目录职责、路由、索引、模板和应用知识
- `docs/changes/` 与 `docs/postmortem/` 的目录、说明和模板
- 从当前代码或用户明确确认中得到的项目知识

除非用户另行明确要求，否则不得修改产品代码、启用应用模块、变更依赖或创建实现决策。

## 工作流程

### 1. 确认来源与目标

确认工作区根目录并检查 `git status`，判断当前属于模板的新副本、正在接入知识体系的已有项目，还是需要重新校准的既有知识库。

已有的人工 Change、Postmortem 和知识文件属于项目数据。不能仅因其与模板示例不同就覆盖或删除。

### 2. 识别真实项目

检查构建清单、包清单、启动入口、部署单元、配置文件和实际目录，形成有证据的应用清单。每个候选应用至少识别：

- 稳定且使用小写 kebab-case 的 appCode
- 可独立构建、运行或部署的边界
- 语言、框架和版本
- 启动或运行入口
- 当前模块状态
- 与其他应用的真实关系

必须区分代码已验证事实、用户确认事实和未解决推断。会实质改变目录结构的未决问题应询问用户；其他推断只能进入 `candidate/`。

### 3. 制定初始化矩阵

编辑前明确“保留 / 重建 / 移除 / 暂存”矩阵：

- 保留通用基础设施和已确认的目标项目内容
- 根据目标工作区重建应用知识、索引和路由
- 只有确认属于模板且与目标无关时，才移除自带示例
- 归属不清的用户内容先保留，直到责任边界明确

未经验证，不得把示例应用目录、appCode、版本、模块或证据路径复制到目标项目。

### 4. 初始化 knowledge

使用 `knowledge/template/` 下的普通 Markdown 模板。模板中 `{{初始化:字段}}` 是必须替换的初始化标记；不能原样留在实例文件中。知识类型、应用身份和生命周期由目录表达，不为知识文档添加 YAML Front Matter 或字段注册表。

每个真实应用边界建立 `knowledge/applications/<appCode>/`，并实例化：

- `application-README-template.md` → `README.md`
- `application-INDEX-template.md` → `INDEX.md`
- `application-overview-template.md` → `<appCode>.md`
- `category-INDEX-template.md` → 四类目录的 `INDEX.md`
- `base/`、`feature/`、`rule/`、`tech/` 的 `README.md` → 对应分类职责说明

替换全部占位符后再写入目标目录。应用总览和四类应用知识必须包含标准 `## 证据来源` 表格；本地代码和文档来源写成可校验的 Markdown 链接。四类正式目录只写已确认知识；推断或未决结论写入 `candidate/`。外部资料保留在 `reference/`，不得自动提升为项目事实。

重新生成所有受影响的 INDEX，并按真实文件系统和应用边界更新 ROUTING。Agent 新生成的项目知识未经用户或项目负责人确认，不得从 `candidate/` 移入 `main/` 或 `applications/`。

### 5. 初始化 docs

保持 Change 与 Postmortem 框架业务中立，并保留生命周期目录、README 和模板。

不得虚构初始 Change 或 Postmortem。只有初始化本身确实包含符合触发条件的设计取舍、行为变化或真实事故时，才创建相应记录。

### 6. 验证

运行：

```text
python .agents/skills/knowledge-docs-initializer/scripts/validate_initialization.py .
git status --short
git ls-files --others --exclude-standard
git diff --check
```

结构校验器会检查无自定义 YAML 头约束、目录骨架、本地 Markdown 链接、应用目录、INDEX 完整性和实例化文件中的未完成占位符。模板可以保留契约定义的占位符。

必须同时检查 Git 列出的 tracked 和 untracked 文件；单独执行 `git diff` 无法覆盖新生成文件。

### 7. 交付说明

最终报告至少包含：

- 项目形态和当前应用清单
- 保留、重建、移除和暂存的内容
- 证据来源与未解决问题
- 验证结果
- 尚待确认的候选知识

除非用户同时要求修改应用代码，否则知识库和 docs 初始化完成后停止。

## 不可违反的边界

- 不得让目标项目继承模板中的产品、行业、功能集合或芋道模块选择。
- 不得把上游模块、目录、依赖或参考资料当成目标项目实际采用的证据。
- 不得把未经确认的 Agent 推断直接写入 `main/` 或 `applications/`。
- 不得在缺乏证据和明确范围时覆盖用户已有项目记录。
- 不得在实例化的 application、Change 或 Postmortem 中留下断链、失效 appCode 或未解析模板占位符。
