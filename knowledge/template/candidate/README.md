# 候选知识模板

本目录提供无 YAML 的候选知识正文模板。只有发现可能成为长期知识、但尚未满足正式知识条件的真实内容时，才实例化 `candidate.md`。

实例化规则：

- 保存到 `knowledge/candidate/main/<relative-path>` 或 `knowledge/candidate/applications/<appCode>/<relative-path>`。
- 文件名使用未来正式知识的文件名，不添加 `candidate-` 前缀。
- `README.md` 与 `INDEX.md` 是 candidate 目录的保留导航文件，不能用作候选文件名，也不参与镜像晋升。
- 替换全部 `{{初始化:...}}` 标记，删除不适用的模板说明。
- 如果拟晋升位置无法判断，不得伪造路径；按需建立 `candidate/unclassified/` 并在“拟晋升位置”写 `待分类`。
- 模板只定义候选阶段需要的证据缺口和晋升条件；晋升后按目标正式知识模板重写。
