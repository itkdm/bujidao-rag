# 知识库校验脚本

本目录提供知识库的自包含只读校验入口，不存放业务脚本或元数据管理工具，也不依赖 `.agent/`、`.agents/` 或初始化 Skill 的安装位置。

Python 本地产生的 `__pycache__/` 与 `*.py[cod]` 由本目录的 `.gitignore` 排除，不属于知识库文件。

## 使用方式

在仓库根目录运行：

```text
python knowledge/scripts/validate.py
```

也可以显式指定工作区：

```text
python knowledge/scripts/validate.py D:/path/to/workspace
```

提交前检查暂存区中的归档移动是否保持来源相对路径：

```text
python knowledge/scripts/validate.py --git-staged
```

GitHub Actions 或推送前流程可以检查一个提交范围：

```text
python knowledge/scripts/validate.py --git-range <base>...<head>
```

Pull Request 或分支相对共同基线的比较使用 `<base>...<head>`；push 事件使用真实事件范围 `<before>..<head>`。

当前入口会检查：

- 根级 `AGENTS.md` 遵循全局规范的六个必选章节，存在唯一的精简 knowledge/docs 路由入口，且不复制完整总路由图
- 受管理 Markdown 没有自定义 YAML Front Matter
- 本地 Markdown 相对链接和图片目标存在且不越出工作区
- INDEX 与直接子项一致
- 应用知识的正文证据链接有效
- 应用目录名、总览文件名、“应用编码”、README 与 INDEX 的 appCode 身份一致
- `candidate/` 使用目标镜像目录，候选正文包含拟晋升位置、证据缺口和验证条件
- `personal/` 的内容按稳定 ownerCode 隔离，所有者 README 与目录标识一致，且不预造空所有者或主题目录
- `archive/` 只使用规定的六个镜像根目录
- `knowledge/` 其他位置没有旁路归档目录
- Change 的状态、类型、日期命名、必选 `change.md`、允许附件和状态必选章节符合契约
- Postmortem 位于规定目录，使用日期命名并包含根因、逃逸原因和防线等必选章节
- 使用 `.agent/skills/` 或 `.agents/skills/` 时，initializer 与两个日常 Skill 同根交付，且 SKILL 与 UI 元数据具备最小有效结构
- 暂存区或指定提交范围中的归档操作确实是移动，并严格保留来源内容域与原相对路径
- 实例文件没有遗留模板专用的双花括号初始化标记

结构、链接等只读检查始终执行；Git 变更映射检查仅在显式传入 `--git-staged` 或 `--git-range` 时执行，两种 Git 模式按当前阶段二选一。`--git-staged` 要求 `knowledge/` 没有未暂存或未跟踪改动，避免工作树内容掩盖暂存快照问题。归档和恢复都应先用 `git mv` 完成标准路径移动，再编辑正文；Git 模式会启用重命名与复制识别，并拒绝用两条 A+D 记录代替 Git 可识别的移动。移动后大幅改写可能使 Git 无法识别重命名，应先完成并验证移动，再分步修改正文。

该命令无第三方依赖，可在本地提交或推送前运行。模板仓库通过 `.github/workflows/knowledge-docs-validate.yml` 在相关 push 与 Pull Request 上自动执行当前结构校验和 Git 范围归档校验；新分支首次 push 因没有有效的 `before` 提交，只执行当前结构校验，后续 Pull Request 仍会检查完整变更范围。其他托管平台可调用同一命令接入 CI。仓库不自动修改用户本机 Git Hook。
