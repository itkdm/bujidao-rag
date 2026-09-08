---
name: knowledge-docs-maintenance
description: 维护已经初始化的 AGENTS.md、knowledge/ 与 docs/ 时使用，包括审查或修正知识、录入 reference/personal、创建或晋升 candidate、归档或恢复知识、维护 INDEX/ROUTING，以及校正 Change/Postmortem 生命周期结构。按各目录权威 README 执行并运行自带校验；不用于首次初始化，也不负责实现产品代码。
---

# 知识库与研发文档维护

在不重新初始化项目、也不修改产品实现的情况下，安全维护知识和研发文档的分类、生命周期、导航与引用完整性。

## 适用边界

本 Skill 处理已经初始化的知识与文档资产。首次接入、应用边界重建或技术栈重新识别使用 `knowledge-docs-initializer`；代码理解、设计、审查和实现使用 `knowledge-driven-development`。任务同时包含代码与知识修改时，由开发 Skill 主导，完成实现后再按本 Skill 的生命周期规则闭环。

先区分只读审查与用户已授权的维护操作。只读任务只报告问题和建议，不写文件；维护任务只修改用户放入范围内的 AGENTS、knowledge、docs、项目级知识 Skill 或校验基础设施，不扩大到产品代码。

## 工作流程

### 1. 路由维护对象

完整读取 `knowledge/README.md` 与 `knowledge/ROUTING.md`，再读取目标目录的 README。只加载当前操作需要的最小内容：

- 正式知识：读取 `main/README.md` 或 `applications/README.md` 及目标分类 README。
- 候选知识：读取 `candidate/README.md` 和拟晋升目标的分类规则。
- 个人素材：读取 `personal/README.md` 与所有者目录 README。
- 外部资料：读取 `reference/README.md`。
- 知识归档或恢复：读取 `archive/README.md`。
- Change 生命周期：读取 `docs/changes/README.md`。
- Postmortem：读取 `docs/postmortem/README.md`。

不得把 reference、candidate、personal、archive、rejected Change 或 archived Change 当作当前项目事实。

### 2. 选择唯一操作

根据内容当前身份执行一种主操作，避免复制后形成双重事实源：

- 新增或纠正正式知识：必须有当前代码、正式文档或负责人确认作为证据，并写入唯一合适的 main/application 分类。
- 新增候选：使用目标镜像路径与候选模板；只有证据、范围或确认尚未闭环但确有长期复用价值时创建。
- 晋升候选：先满足验证条件；目标不存在时移动并改写成正式结构，目标存在时合并后移除候选。
- 候选退出：已证明错误或停止推进且需追溯时归档，否则按用户授权删除无保留价值的内容。
- 录入个人或参考资料：保留来源身份，不自动提升为正式结论。
- 归档或恢复：保持来源内容域和原相对路径，使用移动而非复制，不覆盖既有历史。
- Change 或 Postmortem：只调整真实实例及其生命周期，不为展示目录完整性虚构记录。

涉及项目级 Skill 的创建或实质修改时，同时使用宿主提供的 Skill 创建能力；本 Skill 只约束它与知识体系的衔接、链接和校验，不复制 Skill 编写规范。

### 3. 维护导航与单一权威

新增、移动、重命名或删除后，同步更新直接父目录 INDEX、受影响的上级 INDEX、ROUTING 精确路径和所有真实相对链接。README 只维护稳定职责，不写动态文件清单；同一规则或事实只保留一个权威正文，其他位置使用链接。

修改 AGENTS 时遵循 [AGENTS.md 全局规范](../../../knowledge/main/rules/AGENTSmd%20全局规范.md)，只保留自动加载入口、长期项目事实和硬约束，不把知识正文或完整路由图复制进去。

### 4. 验证与审查

维护完成后运行：

```text
python knowledge/scripts/validate.py
git diff --check
git status --short
```

发生知识归档或恢复移动时，在暂存对应移动后再运行 `python knowledge/scripts/validate.py --git-staged`；CI 中 Pull Request 使用 `--git-range <base>...<head>`，push 事件使用 `--git-range <before>..<head>`。

同时检查 Git 列出的未跟踪文件，避免漏掉新文档。项目规则要求独立审查时，提交前交给独立审查者并合理处理意见。

## 交付要求

说明维护了什么、内容为何放在该位置、采用了什么证据、有哪些移动或生命周期变化、验证结果以及仍需确认的候选问题。只读审查明确区分必须修复项与可延后建议。

## 不可违反的边界

- 不让未经确认的内容进入正式知识。
- 不用复制代替晋升、归档、恢复或生命周期移动。
- 不让 README 和 INDEX 重复维护动态清单。
- 不把临时 TODO、任务计划或实现过程塞入 candidate。
- 不在知识或文档中写入密码、Token、API Key、私密通信、个人隐私或本机专属凭据。
