# AGENTS.md

## 项目概述

- **项目名称**：`bujidao-rag`
- **项目定位**：以芋道系列开源项目作为现成示例，维护可复用的项目知识库与研发文档体系；不预设行业、产品或具体业务。
- **当前形态**：前后端分离的单体应用，后端为 Spring Boot 多模块工程，前端为 Vue3 管理后台。
- **应用组成**：
  - `ruoyi-vue-pro/`：基于芋道 `master-jdk17` 基线的后端工程。
  - `yudao-ui-admin-vue3/`：Vue3 管理后台。
  - `knowledge/`：长期知识、候选知识、个人素材、外部参考、模板和归档。
  - `docs/`：研发变更记录与事故复盘。

目录存在、上游文档存在或模块出现在注释中，不代表对应能力已经启用。代码、构建清单和运行配置是实现事实。

---

## 技术栈

### 后端（ruoyi-vue-pro）

| 技术 | 当前版本或约束 | 说明 |
| --- | --- | --- |
| JDK | 17 | 编译与运行版本 |
| Spring Boot | 3.5.15 | 应用开发框架 |
| Maven | 多模块聚合 | 构建与依赖管理 |
| MyBatis Plus | 3.5.16 | 数据访问 |
| Redisson | 4.6.1 | Redis 客户端 |
| JUnit 5 + Mockito | 以构建配置为准 | 测试框架 |

其余依赖的精确版本以 `ruoyi-vue-pro/yudao-dependencies/pom.xml` 为准。Spring Boot 3 使用 `jakarta.*` 命名空间。

### 前端（yudao-ui-admin-vue3）

| 技术 | 当前版本或约束 | 说明 |
| --- | --- | --- |
| Node.js | `>= 20.19.0` | 运行环境 |
| pnpm | `>= 8.6.0` | 唯一允许的包管理器 |
| Vue | 3.5.34 | 前端框架 |
| Vite | 8.1.4 | 构建工具 |
| TypeScript | 6.0.3 | 类型系统 |
| Element Plus | 2.13.7 | UI 组件库 |

---

## 目录与模块职责

| 路径 | 职责 |
| --- | --- |
| `ruoyi-vue-pro/yudao-dependencies/` | 后端依赖版本统一管理 |
| `ruoyi-vue-pro/yudao-framework/` | Web、Security、Redis、MyBatis 等通用框架能力 |
| `ruoyi-vue-pro/yudao-server/` | 后端应用启动入口与模块装配 |
| `ruoyi-vue-pro/yudao-module-system/` | 当前启用的系统功能模块 |
| `ruoyi-vue-pro/yudao-module-infra/` | 当前启用的基础设施模块 |
| `yudao-ui-admin-vue3/src/api/` | 前端接口定义 |
| `yudao-ui-admin-vue3/src/views/` | 前端页面视图 |
| `yudao-ui-admin-vue3/src/components/` | 前端公共组件 |
| `knowledge/` | 跨任务长期有效的知识与资料 |
| `docs/changes/` | 一次研发变更的提议、实施和历史状态 |
| `docs/postmortem/` | 已发生且暴露系统性防线缺口的问题复盘 |
| `.agents/skills/knowledge-docs-initializer/` | 按目标项目事实初始化 AGENTS、knowledge 与 docs |
| `.dev-tmp/` | 本地调试日志与临时脚本，不进入版本库 |

根 `pom.xml` 当前只聚合 `system` 与 `infra` 业务模块。其他 `yudao-module-*` 目录或被注释的模块均按未启用处理，启用状态必须同时核对根聚合构建、`yudao-server` 运行装配和环境配置。

---

## 运行与开发方式

### 后端

必须使用 JDK 17。

```bash
cd ruoyi-vue-pro
mvn clean install -DskipTests

cd yudao-server
mvn spring-boot:run -DskipTests
```

后端环境配置位于 `ruoyi-vue-pro/yudao-server/src/main/resources/`。不得把本机路径、连接凭据或环境秘密写入 AGENTS、knowledge 或 docs。

### 前端

```bash
cd yudao-ui-admin-vue3
pnpm install
pnpm dev
```

前端统一使用 `pnpm`，禁止使用 `npm` 或 `yarn` 安装依赖。环境与构建命令以 `package.json` 为准。

---

## 验证策略

### 后端

| 验证类型 | 命令 | 适用场景 |
| --- | --- | --- |
| 编译检查 | `mvn clean compile` | 后端代码修改后 |
| 单元测试 | `mvn test` | 业务逻辑修改后 |
| 全量构建 | `mvn clean install -DskipTests` | 公共能力、依赖或发布前 |

### 前端

| 验证类型 | 命令 | 适用场景 |
| --- | --- | --- |
| ESLint | `pnpm lint:eslint:check` | 脚本与组件修改后 |
| 格式检查 | `pnpm lint:format:check` | 文本格式修改后 |
| 样式检查 | `pnpm lint:style:check` | 样式修改后 |
| 类型检查 | `pnpm ts:check` | 类型相关修改后 |
| 全量 lint | `pnpm lint` | 提交前 |
| 构建验证 | `pnpm build:local` | 公共能力或发布前 |

### 知识库与研发文档

```bash
python knowledge/scripts/validate.py
git diff --check
git status --short
```

发生归档或恢复移动时，再按阶段运行 `python knowledge/scripts/validate.py --git-staged`，或在 CI 中运行 `python knowledge/scripts/validate.py --git-range <base>...<head>`。

统一原则：优先运行与修改直接相关的最小验证；公共能力、基础设施或跨模块行为变化时扩大范围；不为通过测试改变本来正确的行为；无法执行的验证要明确说明；不得声称执行过实际未执行的验证。

---

## 项目特有规则

1. **后端模块启用**：模块启用状态必须以构建、运行装配和配置三层证据共同确认，不能只根据目录或注释判断。
2. **模块依赖方向**：业务模块可以依赖框架层，框架层不得反向依赖业务模块。
3. **前端包管理器**：只能使用 `pnpm` 安装依赖。
4. **知识分级**：未经确认的可复用结论进入 `knowledge/candidate/`；个人素材进入 `knowledge/personal/<ownerCode>/`；外部资料进入 `knowledge/reference/`。
5. **代码生成**：生成代码后必须人工审查；修改代码生成模板时记录原因和影响。
6. **调试产物**：临时日志与脚本放入 `.dev-tmp/logs/` 或 `.dev-tmp/scripts/`，不得散落在仓库根目录或提交到版本库。
7. **敏感信息**：密码、Token、API Key、私密通信、个人隐私和本机专属凭据不得进入版本库文件或提交信息。
8. **独立审查**：修改 knowledge、docs 或 `knowledge-docs-initializer` Skill 后，提交前必须由独立子 Agent 审查，并合理处理意见。

---

## Git 规范

当前项目没有覆盖团队 Git 规范，直接遵循：

- [Git Branch 全局分支规范](knowledge/main/tech/Git%20Branch%20全局分支规范.md)
- [Git Commit 全局提交规范](knowledge/main/tech/Git%20Commit%20全局提交规范.md)
- [Pull Request 全局规范](knowledge/main/tech/Pull%20Request%20全局规范.md)

---

## 文档规范

### 文档与知识路由

```text
[首次接触项目] ─► [knowledge/README.md]
[每个具体任务] ─► [knowledge/ROUTING.md]
                           ├─ 稳定知识 ─► knowledge/
                           ├─ 研发变更 ─► docs/changes/
                           └─ 事故复盘 ─► docs/postmortem/
```

- 首次接触项目先读 [knowledge/README.md](knowledge/README.md)。
- 每个具体任务开始前必须读 [knowledge/ROUTING.md](knowledge/ROUTING.md)，再加载任务所需的最小文件集合。
- Change 的触发条件和生命周期见 [docs/changes/README.md](docs/changes/README.md)。
- Postmortem 的触发条件和边界见 [docs/postmortem/README.md](docs/postmortem/README.md)。
- 完整分类、读取顺序、写入位置和生命周期以 `knowledge/ROUTING.md` 为唯一权威来源；本文件只维护自动加载入口，不复制完整路由图。
- 移动、归档或重命名文档后，同步更新 INDEX、ROUTING 和全部相对链接，再运行知识库校验。

---

## 常见风险

1. **模块表象与实际启用不一致**：上游全量目录长期存在，但当前聚合和配置可能只启用一部分模块。
2. **多环境配置差异**：后端和前端均有多环境配置，切换环境时需重新核对。
3. **知识与实现漂移**：详细版本、模块状态和证据入口分别见 [ruoyi-vue-pro 应用总览](knowledge/applications/ruoyi-vue-pro/ruoyi-vue-pro.md) 与 [yudao-ui-admin-vue3 应用总览](knowledge/applications/yudao-ui-admin-vue3/yudao-ui-admin-vue3.md)，修改实现后应同步更新相关知识。

---

## 子级 AGENTS.md

当前项目暂未创建子目录级 `AGENTS.md`。只有子目录存在独立且长期有效的局部约束时才增加；子级文件只记录局部差异，不复制根级规则。

---

## 维护说明

- 本文件遵循 [AGENTS.md 全局规范](knowledge/main/rules/AGENTSmd%20全局规范.md)。
- 只记录当前项目可验证、长期有效、未来任务仍需知道的信息。
- 已失效内容直接更新或删除，不通过追加说明保留旧规则。
