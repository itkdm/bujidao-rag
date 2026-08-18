---
# 知识库导航基础设施文件
id: KB-INFRA-GLOBAL-ARCHIVE-README
scope: global
status: OFFICIAL
owner: bujidao
maintainers:
- bujidao
version: 1
updatedAt: 2026-08-18
verifiedAt: 2026-08-18
tags:
- navigation
- global
anchors:
- GLOBAL:ARCHIVE-README
---

# Archive

## 目录定位

`archive/` 用于保存已经退出当前有效知识体系、但仍有历史参考或追溯价值的内容。

归档内容原则上不再作为 Coding Agent / 开发任务的默认有效知识来源。

## 应包含的内容

- 已被新知识替代的旧版本知识
- 已失效但仍需保留历史记录的规则
- 已废弃应用或模块的历史知识
- 需要保留用于审计、追溯、对比的旧资料
- 从当前 Knowledge 主路径中移出的历史内容

## 不应包含的内容

- 当前仍然有效的知识不得放入 archive
- 尚未确认的知识应进入 candidate，而不是 archive
- 个人临时知识应进入 personal
- 外部原始参考资料应进入 reference
- 正常有效的全局知识和应用知识仍放在原有知识目录

## 维护规则

- 只有已经确认退出当前有效知识体系的内容才允许归档。
- 归档不等于删除。
- 被归档知识默认不得作为当前实现依据。
- 如果归档知识重新恢复有效，应迁回对应正式目录，而不是直接在 archive 中长期维护。
- 后续真正出现归档内容时，再根据实际内容逐步完善目录结构。

## 补充说明

本阶段 archive 目录暂时可能没有实际归档知识文件。

当前先建立 README + INDEX，使其成为正式的 Knowledge 受管理目录。

不要为了「目录完整」创建虚假的归档知识。
