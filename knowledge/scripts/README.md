# validate_metadata.py

对 `knowledge/` 下受管理的 Markdown 文件执行 **只读** Front Matter 元数据校验。

> 唯一规范来源：`../KNOWLEDGE-METADATA-RULES.md`
> 本脚本**绝不修改任何 Markdown 文件**，只输出报告。

## 用途

根据已经确定的元数据规则，扫描 `knowledge/**/*.md`（排除 `reference/` 和 `template/`），
发现明确的 Schema 错误与可疑的历史字段。

## 安装依赖

```bash
pip install -r requirements.txt
```

仅需 `PyYAML`（无其他第三方依赖）。

## 运行命令

```bash
# 普通模式：只显示 ERROR / WARNING 与统计
python knowledge/scripts/validate_metadata.py

# 详细模式：额外打印所有 PASS 文件
python knowledge/scripts/validate_metadata.py --verbose
```

脚本会自动定位仓库根目录、`knowledge/` 目录以及 `KNOWLEDGE-METADATA-RULES.md`。

## ERROR / WARNING 含义

### ERROR（违反已确定的 Schema）

- 缺少全局必填字段（id / scope / status / owner / maintainers / version / updatedAt / verifiedAt / tags / anchors）
- 无 Front Matter 或 YAML 解析失败
- `id` 格式非法或全局重复
- `scope` / `status` / `confidence` / `stability` 非法枚举值
- `appCode` 未注册，或 `scope=global/cross-app` 时误出现
- `owner` / `maintainers` 不在注册表
- `version` 非法（非整数、< 1、bool）
- `updatedAt` / `verifiedAt` 非法日期，或 `verifiedAt > updatedAt`
- `tags` / `anchors` 格式非法，或 anchor 命名空间未注册
- 知识文件（`type` 存在）缺少 `type` / `confidence` / `stability` / `evidence` 或取值非法

### WARNING（不确定是否应报错，不计入失败）

- 未知历史字段（如 `domain` / `application` / `topic` 等）
- `evidence` 条目带有规范未要求的额外字段

## 退出码

- `0`：无 ERROR（允许有 WARNING）
- `1`：存在任意 ERROR

适合未来接入 GitHub Actions：ERROR 即失败。
