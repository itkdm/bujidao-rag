---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-MAIN-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 3
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- global
anchors:
- GLOBAL:MAIN-README
---

# main/

## 目录定位

`knowledge/main/` 存放**跨应用、跨系统、跨业务线**的通用知识。核心判断标准是「是否跨应用强制统一」。例如：业务域内的核心术语；跨应用流程；通用状态定义；全局技术约束；多应用都要遵守的业务规则。

## 应包含的内容

- 跨多个应用都一致、需要统一遵守的术语、概念与状态定义。
- 跨应用共享的通用流程与协作规范。
- 跨应用生效的全局技术约束与基础设施约定。

## 不应包含的内容

- 只影响单个应用的知识：应进入对应 `applications/{appCode}/` 的相应子目录（feature / rule / tech / base）。
- 未经确认的 AI 推断：应先放入 `candidate/`，不要直接写入本目录。
- 个人经验或踩坑记录：应放入 `personal/`，确认后再进入正式目录。

## 维护规则

- 能否放入 `main/` 的核心标准是「是否跨应用强制统一」，单一应用相关的知识不放入本目录。
- AI 在需求执行中分析出的推断，**先放 `candidate/`**。
- 经 owner 明确说明并确认且具备稳定性后，才合并到 `main/`。
- **禁止** AI 直接将未确认内容写入 `main/`；**禁止**所有自动化流程自行判断是否合并到 `main/`。
- **禁止** AI 将个人经验直接当作团队结论引用。
