
# Archive

## 目录定位

`archive/` 保存已经退出当前有效知识体系、但仍有追溯价值的内容。它是 `knowledge/` 内容目录的微缩镜像，不是默认知识来源。

## 目录映射

| 原路径 | 归档路径 |
| --- | --- |
| `knowledge/main/<relative-path>` | `knowledge/archive/main/<relative-path>` |
| `knowledge/applications/<relative-path>` | `knowledge/archive/applications/<relative-path>` |
| `knowledge/candidate/<relative-path>` | `knowledge/archive/candidate/<relative-path>` |
| `knowledge/personal/<relative-path>` | `knowledge/archive/personal/<relative-path>` |
| `knowledge/reference/<relative-path>` | `knowledge/archive/reference/<relative-path>` |
| `knowledge/template/<relative-path>` | `knowledge/archive/template/<relative-path>` |

归档时保留来源目录之后的相对路径。例如：

```text
knowledge/applications/demo/tech/old-design.md
→ knowledge/archive/applications/demo/tech/old-design.md
```

`archive/` 不递归镜像自身；根级 `README.md`、`INDEX.md`、`ROUTING.md` 和校验脚本属于知识库基础设施，不作为普通知识归档。六个来源内容域根部的 `README.md` 与 `INDEX.md` 也属于导航基础设施，只在原位更新，历史由 Git 保留，不能移动到已被归档导航文件占用的同名路径。`docs/` 使用自己的生命周期目录，不移动到这里。

## 归档流程

1. 确认内容已经退出当前有效知识路径；未确认内容仍放 `candidate/`。
2. 对已跟踪文件使用 `git mv` 移入对应镜像目录，不能复制一份后让旧文件继续作为有效知识存在。
3. 保留来源目录之后的相对层级；需要的新子目录按实际归档内容创建，不预造应用、模块或分类。
4. 更新原目录与归档目录的 `INDEX.md`，并检查 `ROUTING.md` 是否仍把该文件作为默认入口。
5. 更新所有应继续指向该内容的相对链接；如果应改指替代知识，则直接链接替代文件。
6. 运行 `python knowledge/scripts/validate.py` 检查结构、索引和相对链接；如果本次实际移动了归档文件，再运行 `python knowledge/scripts/validate.py --git-staged` 检查 Git 移动映射。

## 维护规则

- 当前仍有效的知识不得放入 `archive/`。
- 归档不等于删除，但归档内容默认不得作为当前实现依据。
- 恢复有效时，应按反向映射迁回正式目录并再次更新引用。
- `knowledge/` 下不得用目录符号链接或 Windows junction 代替真实内容域与归档目录。
- 标准归档路径已有历史文件时，不得覆盖。先把既有归档文件在同一镜像树内改为能区分版本或日期的历史文件名，再把当前来源文件移动到标准映射路径，并在历史文件正文中说明原始路径和归档原因。
- 不为了目录完整创建虚假的归档知识；本目录现有 README 和 INDEX 仅定义基础设施契约。
