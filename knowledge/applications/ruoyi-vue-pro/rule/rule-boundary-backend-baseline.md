
# 后端基线边界规则

## AI 使用摘要

- 适用场景：判断 `ruoyi-vue-pro` 当前能力、评估是否复用上游模块、描述后端现状时
- 关键规则：当前后端是模板仓库中的上游开源基线；目录存在不等于模块启用；示例模块能力不能直接写成目标项目已采用能力
- 关联知识：[ruoyi-vue-pro.md](../ruoyi-vue-pro.md)、[base-module-index.md](../base/base-module-index.md)、[tech-architecture-module-boundary.md](../tech/tech-architecture-module-boundary.md)
- 使用前必须核对：根 `pom.xml`、`yudao-server/pom.xml`、后端应用总览和目标项目当前代码

## 证据来源

| 类型 | 来源 | 说明 |
| --- | --- | --- |
| code | [`ruoyi-vue-pro/pom.xml`](../../../../ruoyi-vue-pro/pom.xml) | 当前根工程模块聚合事实 |
| code | [`ruoyi-vue-pro/yudao-server/pom.xml`](../../../../ruoyi-vue-pro/yudao-server/pom.xml) | 当前启动模块实际依赖事实 |
| code | [`ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java`](../../../../ruoyi-vue-pro/yudao-server/src/main/java/cn/iocoder/yudao/server/YudaoServerApplication.java) | 后端启动入口和扫描范围 |
| doc | [`knowledge/applications/ruoyi-vue-pro/ruoyi-vue-pro.md`](../ruoyi-vue-pro.md) | 当前后端定位为开源基线 |
| doc | [`knowledge/applications/ruoyi-vue-pro/base/base-module-index.md`](../base/base-module-index.md) | 当前启用/未启用模块索引 |

## 规则范围

适用于所有关于 `ruoyi-vue-pro` 示例状态、模块启用和上游能力复用的判断。

## 不适用范围

本文不决定目标项目是否启用任何可选模块，也不定义目标项目最终模块划分。

## 规则正文

| 规则 | 内容 | 依据 |
| --- | --- | --- |
| 基线定位规则 | 当前 `ruoyi-vue-pro/` 只能描述为本模板仓库采用的芋道单体后端示例 | `ruoyi-vue-pro.md`、当前代码 |
| 模块状态规则 | 根 `pom.xml` 中未注释的 `<module>` 只证明参与聚合构建；要认定进入当前运行装配，还必须核对 `yudao-server/pom.xml` 的依赖和相关运行配置 | 两个 POM、当前配置 |
| 目录存在规则 | 可选模块目录存在，不代表这些模块已经参与目标项目构建或运行 | `pom.xml` 当前注释状态 |
| 能力表述规则 | 文档和 AI 回答中不得把上游示例能力直接写成目标项目已确认能力 | 当前代码、目标项目确认 |
| 初始化核对规则 | 复用任何上游模块前，必须核对模块启用、依赖、配置、数据库、菜单权限、API 和数据模型 | `base-module-index.md`、`tech-architecture-module-boundary.md` |

## 例外情况

暂无模板级例外。只有目标项目的当前代码和配置能够证明模块已启用，并同步更新 application、base、tech 和 rule 知识后，相关模块才能被描述为该项目已采用能力。

## 违反规则的风险

- AI 会把上游示例能力误当成目标项目已采用能力，导致错误开发计划。
- 可能错误启用大量未评估模块，引入不需要的表、菜单、任务和依赖。
- 产品文档和技术知识会混淆“当前事实”和“未来目标”，后续追责困难。

## 与其他知识的关系

| 知识类型 | 关系 |
| --- | --- |
| `base/` | 模块启用事实见 `base-module-index.md` |
| `tech/` | 模块边界和启用约束见 `tech-architecture-module-boundary.md` |
| `feature/` | 只写目标项目当前可验证能力，避免把上游示例或未来规划写成现状 |

## 待确认问题

| 问题 | 当前状态 | 影响 |
| --- | --- | --- |
| 目标项目是否新建独立模块 | 待初始化 | 影响后端模块边界 |
| 目标项目启用哪些上游模块 | 待初始化 | 影响构建、配置和数据边界 |

## 变更历史

| 版本 | 日期 | 变更内容 | 变更人 |
| --- | --- | --- | --- |
| 1 | 2026-08-09 | 初始版本 | 布吉岛 |
| 3 | 2026-08-23 | 移除具体业务耦合，并校准模块聚合与运行装配边界 | Codex |
