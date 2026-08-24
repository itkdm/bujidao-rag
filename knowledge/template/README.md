# template/

## 目录定位

`knowledge/template/` 保存初始化与知识写作配方，不是当前项目事实，也不参与默认知识检索。

## 模板分类

- `common/`：根级 AGENTS、README、INDEX 等通用结构模板。
- `applications/`：应用总览和 base、feature、rule、tech 分类模板。
- `candidate/`：候选知识正文与导航模板。
- `personal/`：个人所有者目录模板。

## 维护规则

- 模板使用普通 Markdown，不添加知识文档 YAML Front Matter。
- `{{初始化:字段}}` 是实例化时必须替换的标记；不得原样进入正式知识、Change 或 Postmortem。
- 模板只定义业务中立的结构和判断标准，不预设目标项目的 appCode、技术栈、模块、产品或行业。
- 已被替代但仍需追溯的模板按原相对路径移动到 `knowledge/archive/template/`。
