---
id: KB-TECH-GLOBAL-GIT-BRANCH
type: tech
scope: global
status: OFFICIAL
owner: backend-platform
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
confidence: high
stability: stable
evidence:
- type: doc
  ref: knowledge/main/tech/Git Branch 全局分支规范.md
tags:
- git
- branch
- convention
anchors:
- GLOBAL:GIT-BRANCH
- TECH:GIT
---

# Git Branch 全局分支规范

本规范用于统一 Git 分支的基本命名、使用和管理原则，适用于开发者、团队协作以及 Coding Agent 等开发场景。

本文档属于**全局通用规范**。执行具体项目任务时，应同时检查当前任务要求、项目级规范，以及项目已有且稳定的分支约定。

默认优先级为：

**当前任务明确要求 > 项目级规范 > 项目已有稳定约定 > 全局规范**

其中：

* 更具体的规范可以对上层规范进行补充、细化或覆盖。
* 项目历史只有在能够确认其属于持续、稳定且当前仍有效的约定时，才可作为规范参考。
* 单次、零散、不一致或明显过时的历史分支名称，不应直接视为规范。
* 如果显式规范之间存在无法判断的冲突，或显式规范与当前稳定实践明显矛盾、疑似规范已经过期，应暂停相关操作并提示用户确认。

项目级规范通常可以进一步定义：

* Git Flow、Trunk Based Development 等分支模型
* 基础分支和长期分支
* 发布分支规则
* 特殊分支前缀
* Issue / 工单编号格式
* 分支保护与合并策略

---

## 1. 基本原则

分支应围绕一个明确的开发目标创建。

一个分支原则上只处理一个主要任务，避免同时混入多个无关功能、Bug 修复或重构。

推荐：

```text
feat/user-login
fix/token-expiration
refactor/search-service
docs/deployment-guide
```

不推荐：

```text
dev
test
new
temp
my-branch
update
branch1
```

分支名称应让开发者或 Agent 在不查看代码的情况下，大致判断该分支的用途。

---

## 2. 分支命名格式

在项目没有其他明确规范或稳定历史习惯时，推荐：

```text
<type>/<description>
```

例如：

```text
feat/user-login
fix/order-validation
refactor/cache-service
docs/api-guide
```

如果项目需要关联 Issue、任务或工单，可以扩展为：

```text
<type>/<issue-id>-<description>
```

例如：

```text
feat/123-user-login
fix/456-token-expiration
```

如果仓库已经长期稳定采用其他格式，应优先保持项目一致性。

---

## 3. Type 类型

推荐使用以下常见类型：

| Type       | 含义        |
| ---------- | --------- |
| `feat`     | 新功能       |
| `fix`      | Bug 修复    |
| `refactor` | 代码重构      |
| `perf`     | 性能优化      |
| `docs`     | 文档修改      |
| `test`     | 测试相关修改    |
| `build`    | 构建系统或依赖修改 |
| `ci`       | CI/CD 修改  |
| `chore`    | 其他维护性修改   |
| `hotfix`   | 紧急问题处理    |

项目可以根据实际情况补充其他类型，但应保持语义明确且命名一致。

---

## 4. Description

`description` 应简短说明分支目标。

推荐：

```text
feat/password-reset
fix/duplicate-login
refactor/document-parser
```

在没有其他项目约定时，建议：

* 使用英文
* 使用小写字母
* 单词之间使用 `-`
* 描述具体目标
* 避免无意义缩写
* 避免过长名称

不推荐：

```text
feat/add_some_new_user_login_feature
fix/bug
fix/problem
feature/new
update/code
```

不要在同一项目中无规则混用：

```text
-
_
camelCase
PascalCase
```

如果项目历史已经形成稳定分隔符或命名风格，应保持已有一致性。

---

## 5. 一个分支对应一个主要目标

例如：

```text
feat/user-profile
```

不应同时包含：

* 用户资料功能
* 搜索模块重构
* 无关 README 修改
* 无关依赖升级

判断是否需要拆分，可以考虑：

> 如果其中一个修改被取消，其他修改是否仍可以独立开发和合并？

如果可以，通常应考虑拆分分支。

---

## 6. 分支生命周期

任务型分支完成合并后，应及时清理。

通常包括：

```text
feat/*
fix/*
refactor/*
docs/*
test/*
```

长期存在的分支，例如：

```text
main
master
develop
release/*
```

是否使用以及具体含义，应由项目级策略或已有稳定实践决定。

全局规范不强制指定具体分支模型。

---

## 7. 创建分支前

创建新分支前，应：

* 确认当前任务目标
* 检查项目是否存在分支规范
* 查看仓库当前主要分支结构
* 参考近期稳定的分支命名习惯
* 从项目规定的正确基础分支创建
* 尽量基于最新代码创建
* 避免重复创建已有目标的分支

Coding Agent 不得仅根据全局模板自行假设基础分支、分支模型或发布流程。

---

## 8. 分支使用要求

开发过程中：

* 不应持续堆积多个无关任务
* 不应擅自重写他人正在使用的公共分支历史
* 不应随意删除他人分支
* 不应把临时调试内容带入正式合并
* 应保持分支内容与分支目标一致

如果任务范围发生明显变化，应重新判断是否需要拆分新的分支。

---

## 9. 敏感信息

分支名称不得包含：

* 密码
* Token
* API Key
* Secret
* 私钥信息
* 用户敏感信息
* 生产环境敏感数据

分支名称可能被远程仓库、CI/CD、日志及其他系统长期记录，因此应视为工程元数据。

---

## 10. 推荐示例

```text
feat/user-registration
feat/document-upload

fix/token-expiration
fix/order-validation

refactor/search-service
refactor/cache-layer

perf/query-cache

docs/deployment-guide

test/user-service

build/upgrade-dependencies

ci/release-workflow

chore/remove-unused-config
```

---

## 11. 创建前检查

创建分支前，应至少确认：

* 是否已经理解当前任务
* 是否存在项目级分支规范
* 是否存在稳定且当前有效的历史命名习惯
* 基础分支是否正确
* 分支类型是否准确
* 分支名称是否能够表达任务目标
* 是否已有相同或高度重复的分支
* 是否存在无法判断的规范冲突

核心原则：

1. **分支名称能够表达开发目标**
2. **一个分支聚焦一个主要任务**
3. **优先保持当前项目的一致性**
4. **任务型分支完成后及时清理**
5. **具体分支模型由项目决定**
6. **存在无法判断的规范冲突时停止并确认**
