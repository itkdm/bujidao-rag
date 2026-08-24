# candidate/applications/

## 目录定位

本目录存放拟晋升到 `knowledge/applications/<appCode>/` 的候选知识。候选按已识别的 appCode 和未来正式相对路径组织，目录本身不表示结论已经确认。

## 应包含的内容

- 已能判断所属应用，但证据、范围或负责人确认尚未闭环的候选基础事实、功能、规则和技术知识。
- 可能影响应用总览，但当前还不能写入正式应用知识的边界结论。

## 不应包含的内容

- 无法判断所属应用或 appCode 的内容：必要时进入 `candidate/unclassified/`。
- 跨应用正式约束的候选：进入 `candidate/main/`。
- 已确认的应用事实：进入正式 `applications/<appCode>/`。

## 维护规则

- appCode 使用小写 kebab-case，并且必须已经存在于正式 `knowledge/applications/`；应用边界尚未确认时进入 `unclassified/`。
- appCode 内保留未来正式相对路径，例如 `base/`、`feature/`、`rule/` 或 `tech/`，但不预造空分类。
- 候选被确认后移入同 appCode 的正式目录；应用归属变化时先修正候选路径和 INDEX。
- 每个新建子目录必须具有 README 与 INDEX，不用单个大文件代替应用和分类边界。
