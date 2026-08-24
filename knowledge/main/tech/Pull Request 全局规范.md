# Pull Request 全局规范

本规范用于统一 Pull Request（以下简称 PR）的基本创建、描述、Review 和合并原则，适用于开发者、团队协作以及 Coding Agent 等开发场景。

对于使用 Merge Request 等名称的平台，可按照同等原则执行。

本文档属于**全局通用规范**。执行具体项目任务时，应同时检查当前任务要求、项目级规范，以及项目已有且稳定的 PR 协作约定。

默认优先级为：

**当前任务明确要求 > 项目级规范 > 项目已有稳定约定 > 全局规范**

其中：

* 更具体的规范可以对上层规范进行补充、细化或覆盖。
* 项目历史只有在能够确认其属于持续、稳定且当前仍有效的约定时，才可作为规范参考。
* 单个历史 PR 或偶发写法不应直接视为规范。
* 如果显式规范之间存在无法判断的冲突，或显式规范与当前稳定实践明显矛盾、疑似规范已经过期，应暂停相关操作并提示用户确认。

项目级规范通常可以进一步定义：

* PR 模板
* Reviewer 要求
* Approval 数量
* Issue 关联方式
* CI 检查要求
* Squash / Merge / Rebase 策略
* 自动合并规则
* 分支保护策略

---

## 1. 基本原则

一个 PR 应对应一个明确、完整且可审查的逻辑修改。

PR 应尽可能做到：

> 可理解、可 Review、可验证、可回滚。

应避免一个 PR 同时包含多个无关的：

* 功能
* Bug 修复
* 重构
* 大面积格式化
* 依赖升级

---

## 2. PR 标题

项目没有其他明确规范或稳定历史习惯时，推荐与 Git Commit 保持一致：

```text
<type>(<scope>): <description>
```

例如：

```text
feat(auth): add password reset support
fix(api): reject invalid request parameters
refactor(api): simplify validation pipeline
docs: update deployment guide
```

没有明确 Scope 时可以省略：

```text
docs: update contribution guide
```

标题应：

* 简洁
* 准确
* 描述实际修改
* 避免模糊表达

不推荐：

```text
update
fix bug
changes
code update
some fixes
final fix
```

如果项目长期采用其他 PR 标题格式，应保持当前项目的一致性。

---

## 3. PR 描述

PR 描述至少应帮助 Reviewer 理解：

1. 修改了什么
2. 为什么修改
3. 如何验证

简单 PR 可以使用：

```text
## Summary

Add validation for expired refresh tokens.

## Verification

- Added unit tests
- Ran authentication test suite
```

复杂修改可以根据需要补充：

* Background
* Changes
* Design Decisions
* Risks
* Compatibility
* Breaking Changes
* Screenshots
* Migration Notes

不要为了满足模板而机械填写没有实际信息的章节。

---

## 4. 一个 PR 聚焦一个逻辑修改

例如不建议：

```text
feat: add user profile and refactor search and update dependencies
```

更合理的是根据逻辑关系拆分：

```text
feat(user): add user profile
refactor(search): simplify query pipeline
build: upgrade dependencies
```

如果不同修改：

* 可以独立 Review
* 可以独立合并
* 可以独立回滚

通常就应该考虑拆成不同 PR。

---

## 5. 控制 PR 大小

PR 应保持在 Reviewer 能够完整理解的范围内。

大型需求可以按照：

* 独立能力
* 模块
* 实现阶段
* 可部署阶段
* 可验证阶段

进行拆分。

但也不要为了追求“小 PR”而将一个完整逻辑强行拆成大量无法独立理解的碎片。

判断标准不是固定代码行数，而是：

> Reviewer 是否能够清楚理解这次修改的目的、实现和影响。

---

## 6. 避免混入无关变更

PR 中不应无理由混入：

* 无关格式化
* 无关重构
* 无关文件重命名
* 无关文档修改
* 无关依赖升级
* 临时调试代码

例如：

```text
fix(auth): reject expired token
```

就不应该顺便格式化整个项目。

确实需要的额外修改，应判断是否需要独立 PR。

---

## 7. 测试与验证

PR 作者应说明**实际执行过的验证**。

例如：

```text
## Verification

- Added unit tests for token validation
- Ran authentication test suite
- Verified login flow locally
```

不得在未执行的情况下声称：

```text
All tests passed
```

Coding Agent 同样只能报告：

* 实际执行的命令
* 实际执行的测试
* 实际观察到的结果

不得根据推测声称构建、测试或功能已经通过。

---

## 8. 创建 PR 前检查

提交 PR 前，应至少确认：

* 已理解当前任务要求
* 已检查项目级 PR 规范
* 已参考近期稳定的 PR 协作方式
* 修改已经完成必要验证
* 没有明显无关变更
* 没有残留调试代码
* 没有误提交敏感信息
* Commit 基本清晰
* PR 标题准确
* PR 描述能够解释修改
* 项目要求的测试或静态检查已经执行
* 未执行的检查已经明确说明
* 不存在无法判断的规范冲突

---

## 9. Review 过程

PR 作者应：

* 回应 Reviewer 提出的问题
* 对修改建议进行确认
* 对不同意见说明理由
* 修改代码后同步必要说明
* 重要设计发生变化时更新 PR 描述

Reviewer 应重点关注：

* 正确性
* 可维护性
* 可读性
* 安全性
* 测试
* 兼容性
* 架构影响

具体 Review 行为要求由独立的 Code Review 规范定义。

---

## 10. 合并要求

PR 合并前至少应满足：

* 修改目标明确
* 必要 Review 已完成
* 必要检查已通过
* 阻塞性问题已解决
* 不存在已知严重缺陷
* 不包含敏感信息
* 符合当前项目合并策略

以下内容不由全局规范统一规定：

* Approval 数量
* 是否必须 Squash
* Merge / Rebase 方式
* CI 必须通过哪些 Job
* 谁拥有最终合并权限

这些应由项目级规范或当前项目稳定流程决定。

---

## 11. Draft PR

尚未达到正式 Review 条件的修改，可以使用 Draft PR。

适合：

* 提前展示实现方向
* 请求早期设计反馈
* 大型需求分阶段开发
* 提前运行 CI
* 多人协作同步进度

进入正式 Review 前，应重新检查 PR 内容和描述。

---

## 12. Breaking Change

如果 PR 包含不兼容修改，应显著说明。

例如：

```text
## Breaking Changes

The document upload API now returns DocumentResponse
instead of UploadResult.
```

常见情况包括：

* 公共 API 修改
* 参数变化
* 返回结构变化
* 配置项删除
* 协议变化
* 数据结构变化
* 无法向后兼容的行为变化

不得把重要 Breaking Change 隐藏在普通实现说明中。

---

## 13. 安全要求

PR 不得包含：

* 密码
* Token
* API Key
* Secret
* 私钥
* 真实生产环境凭据
* 不必要的用户敏感信息
* 真实生产数据

如果敏感信息已经进入 Git 历史，仅从当前 PR 删除通常不足以解决问题，应按照对应安全流程处理。

---

## 14. 推荐 PR 结构

简单 PR：

```text
## Summary

Briefly describe what changed.

## Verification

- Describe tests or checks actually performed.
```

复杂 PR 可以根据需要扩展：

```text
## Summary

## Background

## Changes

## Verification

## Breaking Changes

## Notes
```

不要求保留没有实际内容的空章节。

---

## 15. 核心原则

1. **一个 PR 聚焦一个主要逻辑修改**
2. **标题和描述能够准确表达修改内容**
3. **保持当前项目已有的稳定协作习惯**
4. **避免混入无关变更**
5. **PR 大小应便于完整 Review**
6. **只报告实际执行过的验证结果**
7. **Breaking Change 必须明确说明**
8. **存在无法判断的规范冲突时停止并确认**
