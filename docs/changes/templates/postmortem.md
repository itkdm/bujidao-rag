# Postmortem: <简短标题>

- 创建日期：YYYY-MM-DD
- 作者：<作者 / Agent>
- 关联 Change：<若已产生整改 Change，填路径；否则写「待定」>

> 模板依据 `docs/changes/README.md` 第 11 节。Postmortem 不是 Change，不写「怎么修」，只写「为什么逃过防线 + 以后怎么让同类问题更早失败」。

## Executive Summary

一句话结论 + 影响范围。

## Impact / What Happened

- 发生了什么
- 影响范围（环境 / 数据 / 用户 / 发布版本）

## Timeline（推荐，可简化）

- 大型事故：发布 → 报错 → 告警 → 定位 → 回滚 → 根因确认（带时间点）
- 普通 Bug：发现 → 初步误判 → 排查 → 根因确认 → 修复

## Root Cause

真正根因。重点描述**机制**，而非某行代码。

## Why It Escaped

### Tests

- 为什么单元测试 / 集成测试没发现

### Review

- 为什么 Code Review 没发现

### Tooling / CI

- 为什么 CI / 类型系统 / 静态检查没阻止

### Process / Rules

- 为什么现有规范 / 流程没覆盖

## Guardrails

> 不要写「以后要更细心」。每条 Guardrail 必须指明落地形式与对应 Change。

- **Guardrail 1（Test）**：<新增/修改什么测试>
- **Guardrail 2（CI）**：<CI 如何强制>
- **Guardrail 3（Rule）**：<AGENTS.md / 规范需补充什么>
- **Guardrail 4（Tooling）**：<脚本 / 静态检查>

## Related Changes

- `<path/to/change.md>` — <该 Change 落地的 Guardrail>
