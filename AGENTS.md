# AGENTS.md

## 项目概述

- **项目名称**：bujidao-rag
- **项目目标**：基于芋道（ruoyi-vue-pro）精简版脚手架，构建 RAG（检索增强生成）模块。
- **当前主要形态**：前后端分离的单体应用，后端为 Spring Boot 多模块架构，前端为 Vue3 管理后台。
- **应用组成**：
  - `yudao-boot-mini/`：后端服务（精简版，仅含系统功能 + 基础设施模块），后续逐步完善。
  - `yudao-ui-admin-vue3/`：前端管理后台（Vue3 + Element Plus）
  - `knowledge/`：项目知识库，存放跨应用共享的规范、技术文档与参考资料

---

## 技术栈

### 后端（yudao-boot-mini）

| 技术 | 版本 | 说明 |
|------|------|------|
| JDK | 1.8 | 编译与运行版本 |
| Spring Boot | 2.7.18 | 应用开发框架 |
| Maven | - | 构建工具，多模块聚合 |
| MyBatis Plus | 3.5.16 | ORM 框架 |
| MySQL | 5.7 / 8.0+ | 关系数据库 |
| Redis | 5.0 / 6.0 / 7.0 | 缓存与消息队列 |
| Redisson | 4.6.1 | Redis 客户端 |
| Spring Security | 5.8.16 | 安全认证 |
| Lombok | 1.18.42 | 代码简化 |
| MapStruct | 1.6.3 | Bean 转换 |
| Druid | 1.2.28 | 数据库连接池 |
| JUnit 5 + Mockito | - | 单元测试 |

### 前端（yudao-ui-admin-vue3）

| 技术 | 版本 | 说明 |
|------|------|------|
| Node.js | >= 20.19.0 | 运行环境 |
| pnpm | >= 8.6.0 | 包管理器（强制使用） |
| Vue | 3.5.34 | 前端框架 |
| Vite | 8.1.4 | 构建工具 |
| TypeScript | 6.0.3 | 类型系统 |
| Element Plus | 2.13.7 | UI 组件库 |
| Pinia | 3.0.4 | 状态管理 |
| Vue Router | 5.0.6 | 路由 |
| UnoCSS | 66.6.8 | 原子化 CSS |
| ECharts | 6.0.0 | 图表 |

---

## 目录与模块职责

### 根目录结构

```
bujidao-rag/
├── AGENTS.md                  # 本文件，项目级上下文与规则
├── knowledge/                 # 项目知识库（规范、技术文档、参考资料）
├── yudao-boot-mini/           # 后端服务
└── yudao-ui-admin-vue3/       # 前端管理后台
```

### 后端模块（yudao-boot-mini）

| 模块 | 职责 |
|------|------|
| `yudao-dependencies/` | Maven 依赖版本统一管理（BOM） |
| `yudao-framework/` | 框架层，包含多个 Spring Boot Starter（Web、Security、Redis、MyBatis、MQ、WebSocket 等） |
| `yudao-server/` | 应用启动入口，聚合各业务模块 |
| `yudao-module-system/` | 系统功能模块：用户、角色、菜单、部门、租户、字典、短信、邮件、操作日志等 |
| `yudao-module-infra/` | 基础设施模块：代码生成、文件服务、配置管理、定时任务、API 日志、数据库文档等 |
| `sql/` | 数据库初始化脚本 |
| `script/` | 部署脚本、Docker 配置、Jenkins 配置等 |

> 当前精简版仅启用 `system` 和 `infra` 两个业务模块，其他模块（member、bpm、pay、mall 等）已注释。

### 前端目录（yudao-ui-admin-vue3）

| 目录 | 职责 |
|------|------|
| `src/api/` | 后端接口定义（按模块组织） |
| `src/views/` | 页面视图组件 |
| `src/components/` | 公共组件 |
| `src/layout/` | 布局组件 |
| `src/store/` | Pinia 状态管理 |
| `src/router/` | 路由配置 |
| `src/utils/` | 工具函数 |
| `src/hooks/` | 组合式 API hooks |
| `src/directives/` | 自定义指令 |
| `src/plugins/` | 插件配置 |
| `src/styles/` | 全局样式 |
| `src/locales/` | 国际化 |
| `src/assets/` | 静态资源 |

### 知识库（knowledge）

| 目录 | 职责 |
|------|------|
| `knowledge/main/rules/` | 跨应用共享的协作规范（如 AGENTS.md 全局规范） |
| `knowledge/main/tech/` | 跨应用共享的技术知识与约束（如 Git 分支/提交规范） |
| `knowledge/reference/` | 外部参考资料（如芋道官方文档） |

---

## 运行与开发方式

### 后端

```bash
# 进入后端目录
cd yudao-boot-mini

# 安装依赖并编译
mvn clean install -DskipTests

# 本地启动（通过 yudao-server 模块）
cd yudao-server
mvn spring-boot:run
```

- 配置文件位于 `yudao-server/src/main/resources/`，按环境区分（如 `application-local.yaml`、`application-dev.yaml` 等）。
- 数据库初始化脚本位于 `sql/` 目录。
- 环境变量与配置管理：优先使用项目内配置文件，敏感信息通过环境变量注入。

### 前端

```bash
# 进入前端目录
cd yudao-ui-admin-vue3

# 安装依赖
pnpm install

# 本地开发启动
pnpm dev

# 构建
pnpm build:local
```

- 前端使用 `pnpm` 作为包管理器，**禁止使用 npm 或 yarn**。
- 多环境构建：`build:local` / `build:dev` / `build:test` / `build:stage` / `build:prod`。

---

## 验证策略

### 后端

| 验证类型 | 命令 | 适用场景 |
|----------|------|----------|
| 编译检查 | `mvn clean compile` | 代码修改后 |
| 单元测试 | `mvn test` | 业务逻辑修改后 |
| 全量构建 | `mvn clean install -DskipTests` | 发布前 |

### 前端

| 验证类型 | 命令 | 适用场景 |
|----------|------|----------|
| ESLint 检查 | `pnpm lint:eslint:check` | 代码修改后 |
| 格式检查 | `pnpm lint:format:check` | 代码修改后 |
| 样式检查 | `pnpm lint:style:check` | 样式修改后 |
| 全量 lint | `pnpm lint` | 提交前 |
| 类型检查 | `pnpm ts:check` | 类型相关修改后 |
| 构建验证 | `pnpm build:local` | 发布前 |

### 统一原则

- 优先运行与当前修改直接相关的最小验证集合。
- 修改公共能力、基础设施或跨模块行为时扩大验证范围。
- 不为了让测试通过而改变本来正确的业务行为。
- 无法执行某项验证时，应明确说明原因。
- 不声称执行过实际未执行的验证。

---

## 项目特有规则

1. **后端模块扩展**：当前精简版仅启用 `system` 和 `infra` 模块。如需新增业务模块，参考芋道迁移文档，从完整版按需迁移，不要直接复制未使用的模块。
2. **前端包管理器**：强制使用 `pnpm`，禁止使用 `npm` 或 `yarn` 安装依赖。
3. **知识库维护**：`knowledge/` 目录中的规范文档是项目长期约束的来源。修改规范时，应同步更新对应文档。AI 推断的未确认内容不得直接写入 `knowledge/main/`，应先放入 `candidate/`。
4. **代码生成**：后端代码生成模板位于 `yudao-module-infra/src/main/resources/codegen/`，前端代码生成通过管理后台界面操作。生成代码后需人工审查，不要直接合并。
5. **多环境配置**：后端和前端均支持多环境配置，开发时优先使用 `local` 环境。

---

## 架构与分层

### 后端分层

```
Controller
  → Service
    → Mapper
      → Database
```

- **Controller 层**：处理 HTTP 请求，参数校验，返回统一响应格式。
- **Service 层**：业务逻辑处理，事务管理。
- **Mapper 层**：数据访问，基于 MyBatis Plus。
- 框架层（`yudao-framework`）提供通用能力，业务模块（`yudao-module-*`）依赖框架层，不反向依赖。

### 前端分层

```
Views（页面）
  → API（接口调用）
  → Components（公共组件）
  → Store（状态管理）
```

---

## Git 规范

遵循全局 Git 规范，详见：

- 分支规范：`knowledge/main/tech/Git Branch 全局分支规范.md`
- 提交规范：`knowledge/main/tech/Git Commit 全局提交规范.md`
- Pull Request 规范：`knowledge/main/tech/Pull Request 全局规范.md`

核心要点：

- 分支命名：`<type>/<description>`，如 `feat/user-login`、`fix/token-expiration`
- 提交格式：Conventional Commits，`<type>(<scope>): <description>`
- 一个分支聚焦一个主要任务，一个 Commit 对应一个逻辑修改
- description 默认使用英文

---

## 文档规范

- 项目级规范文档统一存放在 `knowledge/` 目录下。
- 跨应用共享的规范放入 `knowledge/main/`。
- 项目特有文档按需创建，避免与全局规范重复。
- 修改规范文档时，应同步更新 `knowledge/main/INDEX.md` 等导航文件。

---

## 禁止事项

1. **禁止**在 `knowledge/main/` 中直接写入未经确认的 AI 推断内容。
2. **禁止**使用 `npm` 或 `yarn` 安装前端依赖，必须使用 `pnpm`。
3. **禁止**直接修改代码生成器生成的模板文件而不记录原因。
4. **禁止**将临时调试代码、日志输出提交到版本控制。
5. **禁止**在分支名称或提交信息中包含敏感信息（密码、Token、API Key 等）。

---

## 常见风险

1. **后端模块依赖方向**：业务模块只能依赖框架层，不能反向依赖。新增模块时注意依赖方向。
2. **前端构建内存**：构建和类型检查命令已设置 `--max_old_space_size=8192`，低内存环境可能构建失败。
3. **多环境配置差异**：后端和前端均有多环境配置，开发、测试、生产环境配置可能不同，切换环境时需确认配置正确。
4. **知识库文档同步**：修改项目规范时，需同步更新 `knowledge/` 中的对应文档，避免规范与实际代码脱节。
5. **精简版与完整版差异**：当前后端为精简版，部分功能模块未启用。如需新增功能，需从完整版迁移或自行开发。

---

## 子级 AGENTS.md

当前项目暂未创建子目录级 `AGENTS.md`。如后续某个子目录存在独立、长期有效的局部约束，可在对应子目录增加 `AGENTS.md`，仅记录局部差异，不复制根级规则。

---

## 维护说明

- 本文件由项目负责人维护，AI 协助更新。
- 修改本文件时，应确保内容已通过当前项目文件或代码确认，或由项目负责人明确确认。
- 不确定内容标记为 `待确认`，尽快完成验证。
- 已失效内容应直接更新或删除，不通过追加"补充说明"保留过期规则。