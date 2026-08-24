# 个人知识目录模板

本目录提供无 YAML 的个人所有者目录模板。只有某个所有者确实产生个人经验、踩坑记录或碎片素材时，才实例化 `{ownerCode}/`；不得为了登记人员预造空目录。

实例化规则：

- 复制 `{ownerCode}/README.md` 与 `{ownerCode}/INDEX.md` 到 `knowledge/personal/<ownerCode>/`。
- ownerCode 是当前仓库内唯一且长期不变的标识，使用小写 kebab-case。
- 真实姓名和昵称只作为显示名称写入 README，不作为必须跟随变化的目录名。
- 必要时使用稳定后缀解决标识冲突；不要把邮箱、手机号或工号直接作为 ownerCode。
- 替换全部 `{{初始化:...}}` 标记，不添加 YAML Front Matter。
- 个人目录至少包含一份真实个人内容；按主题建立子目录时，每个子目录继续使用 README + INDEX 协议。
- 个人素材整理成熟后进入 `candidate/`；不要在 personal 内预造 `main/` 或 `applications/` 镜像。
