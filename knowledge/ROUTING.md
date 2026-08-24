# 路由规则

本文档是知识库的**需求级检索入口**。AI 在每个具体需求开始时，必须先读本文档进行定位。

> **注意**：首次接触知识库时先读取 `README.md`；每个具体需求开始时，再读取本文档进行任务路由。

## 总路由图

```text
[任务 / 待写内容]
        │
        ▼
[首次：README；每次：ROUTING]
        │
        ├─ 研发变更或设计决策 ─────────────► [docs/changes/]（先读 README）
        │      ├─ 新建、讨论中或实施中 ─────► [proposed/] ← [templates/]
        │      ├─ 当前仍有效的决策 ─────────► [implemented/]
        │      ├─ 讨论后未采用 ─────────────► [rejected/]
        │      └─ 已失效或被替代 ───────────► [archived/]
        │
        ├─ 达到 Postmortem 条件的已发生问题 ─► [docs/postmortem/]（先读 README）← [templates/]
        │      └─ 修复或防线落地时，同时建立相关 proposed Change
        ├─ 上游官方材料、外部文章或证据 ─────► [knowledge/reference/]
        ├─ 个人经验、踩坑或碎片素材 ─────────► [knowledge/personal/<ownerCode>/]
        ├─ 显式追溯已退出知识（非 Change） ───► [knowledge/archive/INDEX.md]
        ├─ 知识写作结构或初始化配方 ─────────► [knowledge/template/]
        ├─ 未确认但可能长期复用的结论
        │      ├─ 已知全局目标 ─────────────► [knowledge/candidate/main/<relative-path>]
        │      ├─ 已知应用目标 ─────────────► [knowledge/candidate/applications/<appCode>/...]
        │      └─ 目标范围不明 ─────────────► [knowledge/candidate/unclassified/]（按需建立）
        │
        └─ 已确认且长期有效的项目知识
               ├─ 跨应用统一 ──────────────► [knowledge/main/]
               └─ 单一应用范围 ────────────► [knowledge/applications/<appCode>/]
                      ├─ 当前事实与位置 ────► [base/]
                      ├─ 已实现能力流程 ────► [feature/]
                      ├─ 必须满足的约束 ────► [rule/]
                      └─ 实际实现机制 ──────► [tech/]

[知识目标目录] ─► [README / INDEX / 应用总览] ─► [任务所需的最小文件集]
                                                        │
                                           需要编码时回到当前代码核对
                                                        │
                                           发生知识变更时 ▼
                                  [更新 INDEX / ROUTING / 相对链接]
                                                        │
                                                        ▼
                                  [python knowledge/scripts/validate.py]
```

执行时只加载当前任务需要的最小知识集合。知识缺失时先回到当前代码或已有研发文档核对；只有形成“可能长期复用但尚未确认”的独立结论后才进入 candidate，不能把知识缺口或 TODO 当候选。`feature/` 为空时回到当前代码、相关 Change 或负责人确认。无论知识是否已有，编码前都必须复核当前实现。

## 当前芋道示例的最小读取路径

以下路径只描述本仓库当前两个芋道示例应用。初始化到其他项目时，必须按真实 appCode 和实际存在的知识文件重建本表，不能照搬示例路径。

| 任务意图 | 最小读取路径 | 停止条件 |
| --- | --- | --- |
| 新增后端管理接口 | `applications/ruoyi-vue-pro/INDEX.md` → `base/base-api-index.md` → `rule/rule-permission-admin-app-boundary.md` → `tech/tech-framework-web-api.md` → `tech/tech-error-exception-log.md` | 已定位 Controller、权限边界、请求/响应规范、错误码规范 |
| 新增后端表或查询 | `applications/ruoyi-vue-pro/INDEX.md` → `base/base-database-index.md` → `base/base-model-index.md` → `tech/tech-data-mybatis-cache.md` | 已定位 SQL、DO、Mapper 规则和查询约束 |
| 新增后端定时任务或消息消费 | `applications/ruoyi-vue-pro/INDEX.md` → `base/base-async-index.md` → `tech/tech-async-job-mq.md` → `tech/tech-error-exception-log.md` | 已定位 Job、MQ 入口、异常处理和重试风险 |
| 判断上游模块能否直接复用 | `applications/ruoyi-vue-pro/INDEX.md` → `ruoyi-vue-pro.md` → `rule/rule-boundary-backend-baseline.md` → 必要时读取 `reference/` 对应证据 | 已确认模块启用状态和基线边界 |
| 修改 Vue3 管理后台 | `applications/yudao-ui-admin-vue3/INDEX.md` → `yudao-ui-admin-vue3.md` → 对应分类 README → 当前代码 | 已确认应用边界和知识覆盖范围；正式知识为空时不自行推断 |
| 梳理已实现功能或运行流程 | 对应应用 `feature/README.md` → 当前代码 → 相关 `docs/changes/` | 已确认事实来自当前实现、已落地 Change 或负责人确认，不把空 feature 当事实 |

## 应用内分类

进入 `applications/<appCode>/INDEX.md` 后，只按问题本质选择一个主分类；需要补充上下文时再跨分类读取。

| 要回答的问题 | 主入口 | 典型线索 |
| --- | --- | --- |
| 当前事实是什么、对象在哪里 | `base/README.md` | 模块、包、Controller、API、DO、VO、表、SQL、配置、权限编码、MQ、Job |
| 当前已经实现了什么能力 | `feature/README.md` | 可观察功能、主要流程、用户可执行操作 |
| 当前必须满足什么约束 | `rule/README.md` | 权限、状态、数据边界、安全例外、配置开关 |
| 当前实际上如何实现 | `tech/README.md` | 架构、框架、事务、缓存、消息、异常、日志、构建、测试 |

需要定位规则涉及的代码对象时，从 rule 转到 base；需要实现规则或能力时，再转到 tech。跨应用统一规则进入 `main/`，一次性个人排查过程进入对应 `personal/<ownerCode>/`。

## 禁止事项

1. 不默认读取整个知识库。
2. 不在未 review 的情况下晋升候选知识。
3. 不把 `candidate/` 当作正常实现依据；读取候选时必须同时核对其证据缺口和晋升条件。
4. 不把功能流程、业务规则、事实索引和技术约束混在同一个知识文件里。
5. 不把项目正式决策混进知识文件；已确认决策应进入 `docs/`。
6. 不将 `archive/` 中的知识作为正常路由结果返回（除非显式追溯历史）。
7. 归档文件必须移动到 `archive/<来源内容域>/<原相对路径>`，并同步更新 INDEX、ROUTING 与相对链接。
