# Git Commit 全局提交规范

本规范用于统一 Git Commit Message 的基本格式与提交原则，适用于开发者、团队协作以及 Coding Agent 等开发场景。

本文档属于**全局通用规范**。执行具体项目任务时，应同时检查当前任务要求、项目级规范，以及项目已有且稳定的提交约定。

默认优先级为：

**当前任务明确要求 > 项目级规范 > 项目已有稳定约定 > 全局规范**

其中：

* 更具体的规范可以对上层规范进行补充、细化或覆盖。
* 项目历史只有在能够确认其属于持续、稳定且当前仍有效的约定时，才可作为规范参考。
* 单次、零散、不一致或明显过时的历史提交，不应直接视为规范。
* 如果显式规范之间存在无法判断的冲突，或显式规范与当前稳定实践明显矛盾、疑似规范已经过期，应暂停相关操作并提示用户确认，不得自行猜测。

项目级规范通常可以进一步补充：

* 可使用的 `scope`
* 特殊提交类型
* Issue / PR 关联方式
* 发布相关要求
* 项目特有的 Commit Message 规则

---

## 1. Commit 格式

统一采用 Conventional Commits 风格：

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

其中：

* `type`：必填，表示提交类型
* `scope`：可选，表示本次修改影响的模块或范围
* `description`：必填，简要描述本次修改
* `body`：可选，用于说明复杂修改的背景、原因或实现方式
* `footer`：可选，用于 Breaking Change、Issue 等信息

示例：

```text
feat(rag): add document reranking support
```

```text
fix(auth): reject expired refresh tokens
```

---

## 2. Type 类型

推荐使用以下类型：

| Type       | 含义                 |
| ---------- | ------------------ |
| `feat`     | 新增功能               |
| `fix`      | 修复 Bug             |
| `docs`     | 文档修改               |
| `style`    | 代码格式调整，不改变代码逻辑     |
| `refactor` | 代码重构，不新增功能、不修复 Bug |
| `perf`     | 性能优化               |
| `test`     | 新增或修改测试            |
| `build`    | 构建系统、依赖或构建配置修改     |
| `ci`       | CI/CD 配置修改         |
| `chore`    | 其他维护性修改            |
| `revert`   | 回滚之前的提交            |

例如：

```text
feat(user): add password reset support
fix(auth): prevent duplicate login requests
docs: update deployment guide
refactor(search): simplify query pipeline
perf(cache): reduce lookup latency
test(user): add login service tests
build: upgrade project dependencies
ci: add pull request validation
chore: remove obsolete configuration
```

应优先使用语义明确的类型，不要把能够归类为 `feat`、`fix`、`refactor`、`build` 等的修改全部写成 `chore`。

---

## 3. Scope

`scope` 用于表示本次修改主要影响的模块、领域或子系统。

例如：

```text
feat(auth): add OAuth login support
fix(user): validate user status before login
refactor(storage): simplify file upload flow
```

Scope 应：

* 简短、稳定
* 使用小写英文
* 优先对应模块、领域或子系统
* 同一范围保持统一命名

不建议：

```text
fix(UserServiceImpl.java): handle null user
```

也不建议：

```text
fix(user-service-login-validation-method): handle invalid state
```

如果没有明确 Scope，可以省略：

```text
docs: update development guide
```

具体项目已经形成稳定 Scope 使用习惯时，应优先保持历史一致性；如果项目提供了明确 Scope 列表，则以项目规范为准。

---

## 4. Description

`description` 应使用一句简洁的话说明：

> 本次 Commit 做了什么。

推荐：

```text
feat(rag): add hybrid search support
fix(auth): prevent expired token refresh
refactor(user): simplify permission validation
```

建议：

* 默认使用英文
* 使用现在时或命令式表达
* 首字母小写
* 末尾不加句号
* 描述具体修改，不使用模糊信息

常用动词：

```text
add
fix
remove
update
support
prevent
simplify
improve
rename
replace
```

避免：

```text
update
fix bug
update code
modify code
some fixes
优化代码
修改代码
提交一下
final
final fix
123
```

Commit Message 应让开发者或 Agent 在不查看 Diff 的情况下，也能大致理解本次修改。

如果项目已有长期稳定的语言习惯，例如始终使用中文 Commit，则应保持项目一致性，而不是为了遵循全局默认规则强行切换。

---

## 5. Body

简单修改通常不需要 Body：

```text
fix(auth): reject expired refresh tokens
```

复杂修改可以增加 Body：

```text
refactor(rag): separate retrieval from generation

Move retrieval logic into a dedicated service to reduce coupling
between document retrieval and response generation.

This also allows retrieval to be tested independently.
```

Body 主要用于说明：

* 为什么修改
* 原来存在什么问题
* 当前方案的重要设计考虑
* 必要的实现背景或影响

不要简单重复代码已经能够表达的信息。

---

## 6. Footer

Footer 可用于 Breaking Change、Issue、PR 等信息。

例如：

```text
fix(auth): reject expired refresh tokens

Fixes #128
```

```text
feat(api): add batch document endpoint

Closes #245
```

具体关联格式由项目级规范或已有稳定实践决定。

---

## 7. Breaking Change

存在不兼容变更时必须明确标记。

可以使用：

```text
feat(api)!: change document response format
```

或者：

```text
feat(api): change document response format

BREAKING CHANGE: the API now returns DocumentResponse instead of UploadResult.
```

常见 Breaking Change 包括：

* 删除或修改公开 API
* 修改 API 参数或返回结构
* 删除配置项
* 修改公共协议
* 修改无法向后兼容的公共行为

普通功能修改不要标记为 Breaking Change。

---

## 8. Commit 粒度

一个 Commit 应尽量对应一个**完整且独立的逻辑修改**。

例如：

```text
fix(auth): prevent duplicate login requests
```

不要把以下互不相关的修改塞进同一个 Commit：

* 修复登录 Bug
* 重构搜索模块
* 修改 README
* 升级依赖

应根据逻辑关系拆分：

```text
fix(auth): prevent duplicate login requests
refactor(search): simplify query pipeline
docs: update architecture guide
build: upgrade project dependencies
```

判断一个 Commit 是否合理，可以考虑：

> 这个修改能否被独立理解、Review 和回滚？

如果不能，通常应该重新拆分。

---

## 9. 按逻辑修改提交

Commit 的单位是**逻辑变更**，而不是文件数量。

一个完整功能即使修改多个文件，也可以属于同一个 Commit：

```text
feat(user): add password reset support
```

反过来，同一个文件中存在两个互不相关的修改，也可以拆成多个 Commit。

不要因为文件数量机械拆分或合并。

---

## 10. 避免混入无关修改

提交某个功能时，不应顺手混入无关的：

* 格式化
* 重构
* 文档调整
* 依赖升级
* 其他模块修改

例如：

```text
feat(rag): add document reranking
```

应只包含完成该逻辑修改所必要的内容。

---

## 11. 提交前检查

创建 Commit 前，应至少确认：

* 是否已经检查当前任务要求
* 是否存在项目级提交规范
* 是否存在清晰、稳定且当前仍有效的历史提交约定
* `type` 是否准确
* `scope` 是否合理
* `description` 是否清晰
* 是否混入无关修改
* 是否需要拆分 Commit
* 是否存在 Breaking Change
* 是否需要关联 Issue / PR
* 是否存在无法判断的规范冲突

常规推荐格式：

```text
<type>(<scope>): <description>
```

核心原则：

1. **类型准确**
2. **描述清晰**
3. **保持项目历史一致性**
4. **一个 Commit 对应一个逻辑修改**
5. **避免混入无关变更**
6. **存在无法判断的规范冲突时停止并确认**
