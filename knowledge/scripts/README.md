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
- 暂存区或指定提交范围中的归档操作确实是移动，并严格保留来源内容域与原相对路径
- 实例文件没有遗留模板专用的双花括号初始化标记

结构、链接等只读检查始终执行；Git 变更映射检查仅在显式传入 `--git-staged` 或 `--git-range` 时执行，两种 Git 模式按当前阶段二选一。`--git-staged` 要求 `knowledge/` 没有未暂存或未跟踪改动，避免工作树内容掩盖暂存快照问题。归档和恢复都应先用 `git mv` 完成标准路径移动，再编辑正文；Git 模式会启用重命名与复制识别，但不会根据两条无关的 A+D 记录猜测移动意图。该命令无第三方依赖，可在本地提交或推送前运行，也可以后续直接接入 GitHub Actions、其他 CI 或团队统一的 pre-push 流程。仓库当前只提供可复用命令，不自动修改用户本机 Git Hook。
