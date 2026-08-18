---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-MAIN-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 2
updatedAt: 2026-08-18
verifiedAt: 2026-08-17
tags:
- navigation
- global
anchors:
- GLOBAL:README
---

# main/定位

`knowledge/main/` 放的是跨应用、跨系统、跨业务线的通用知识。

例如：业务域内的核心术语；跨应用流程；通用状态定义；全局技术约束；多应用都要遵守的业务规则。

能否存放到main文件夹里面核心取决于"是否跨应用强制统一"！

## 知识流转路径

personal/ 个人经验 → candidate/ 候选知识 → owner review → main/ 正式知识
↓
需求执行中被引用 → 代码或业务变化后更新 / 归档 deprecated

- AI 在需求执行中分析出的推断，**先放 `candidate/`**。
- 经 owner 明确说明并确认且具备稳定性后，才合并到 `main/`。
- 如果某条知识只影响单个应用，应进入对应 `applications/`，不要放入 `main/`。
- **禁止** AI 直接将未确认内容写入 `main/`。
- **禁止**所有自动化流程，自动化判断是否合并到 `main/`。
- **禁止** AI 将个人经验直接当作团队结论引用
