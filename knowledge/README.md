
# 知识库

## 目录定位

本知识库是 AI 研发交付底座的**知识资产层**，负责沉淀团队的稳定上下文，为 Coding Agents 提供准确、可路由、可验证的知识来源。

本仓库以芋道系列开源项目作为现成示例，用于展示单体后端、管理后台、模块索引和上游参考资料如何组织；示例不代表目标用户必须采用芋道，也不预设任何行业、产品或具体业务。

整个知识库按分层设计组织，各层目录各司其职：

- `main/`：跨应用、跨系统、跨业务线的通用知识（核心术语、跨应用流程、通用状态定义、全局技术约束、多应用都要遵守的业务规则）。
- `applications/`：按真实构建、运行或部署边界划分的应用知识（应用总览、功能、规则、技术约束、基础事实等）；源码模块归入所属应用，不单独冒充 appCode。
- `candidate/`：按拟晋升路径组织的候选知识队列；只保存可能成为长期知识、但证据或确认条件尚未闭环的内容。
- `personal/`：按仓库内稳定 ownerCode 隔离的个人研发经验和踩坑记录，整理后可转为 candidate 再进正式知识库。
- `template/`：强约束的知识写作模板与导航模板基础设施。
- `reference/`：上游官方文档、外部文章、开源项目说明等证据材料。
- `archive/`：按内容域镜像原相对路径的历史知识，不参与默认检索。

知识库提供稳定上下文；当前代码仍然是实现事实。尤其接口签名、DTO 字段、Topic 配置、feature key、状态枚举、开关配置等易变内容，知识库只提供定位入口，真正改代码前必须回到当前仓库核对真实代码。

## 模板初始化

新项目采用本体系时，应使用项目实际提供的 `knowledge-docs-initializer` Skill（本仓库位于 `.agents/skills/knowledge-docs-initializer/`）。初始化时按目标工作区重新识别应用、技术栈、芋道形态（如适用）、前端版本和启用模块，不得直接继承本仓库示例应用的 appCode、模块状态、版本或证据路径。

## 日常开发驱动

初始化完成后的代码理解、方案设计、代码审查和实现任务使用项目提供的 `knowledge-driven-development` Skill；具体存放目录遵循宿主的项目级 Skill 约定。该 Skill 只负责读取 ROUTING、选择最小知识集合、核对当前代码、执行验证并闭环知识与 Change；具体规范正文继续由 knowledge 与 docs 维护，Skill 不复制第二份规则。宿主不支持项目级 Skill 时，初始化过程删除本节，由根级 AGENTS 直接驱动 README 与 ROUTING。

根级 `AGENTS.md` 只维护自动加载入口、必要项目事实和硬约束；完整 knowledge/docs 路由以 `ROUTING.md` 为唯一权威来源，避免两处重复维护。

当前主分支采用轻量 Markdown：知识身份、类别和生命周期由目录表达，不为受管理文档维护 YAML Front Matter。需要继续研究结构化字段时，使用 `feat/structured-metadata` 分支；首个结构化基线为 `structured-metadata-v0.1` 标签。

这一约束适用于团队自维护的 `knowledge/` 与 `docs/` 文档。`reference/` 中原样导入的外部资料可以保留抓取工具生成的来源追溯头；它们是只读证据，不纳入知识字段维护。

## 应包含的内容

- 各层目录的稳定职责说明与维护契约。
- 跨应用 / 应用内 / 候选 / 个人知识文件（feature、rule、tech、base 等类型）。
- 基础设施文件：`README.md`、`INDEX.md`、`ROUTING.md`、`template/` 和 `scripts/`。

## 不应包含的内容

- 动态文件清单与内容索引：应放在各目录的 `INDEX.md`。
- 用户具体任务路由与 Agent 读取链：应放在 `ROUTING.md`。
- 真实代码实现、未确认的业务推断：推断先入 `candidate/`，不要直接写入正式目录。

## 维护规则

- AI 应通过 `ROUTING.md` 先定位，再按需求关键词、业务身份、状态码、接口名等线索逐步加载正确粒度的上下文，不全量读取。
- 禁止 AI 直接将未确认内容写入 `main/` 或 `applications/`；禁止将个人经验直接当作团队结论引用。
- 知识流转：`personal/` → `candidate/` →（确认）→ `main/` 或 `applications/`；失效知识按原相对路径移动到 `archive/<来源内容域>/`。
- 个人内容只能写入 `personal/<ownerCode>/`；ownerCode 使用仓库内唯一且长期不变的小写 kebab-case，姓名和昵称只作为显示信息。
- 候选知识不是默认事实来源；需要核对知识缺口、来源冲突或待确认结论时，才按 `candidate/main/`、`candidate/applications/` 的目标镜像读取。
- 正式知识必须在正文中写明必要的事实来源，并在修改代码前回到当前实现复核。
- 归档或移动知识后必须更新相关 INDEX、ROUTING 和相对链接，并运行 `python knowledge/scripts/validate.py`。

## 补充说明

`archive/` 的完整路径映射和操作流程见 [`archive/README.md`](./archive/README.md)。
