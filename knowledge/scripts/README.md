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

# metadata_report.py

基于已通过 `validate_metadata.py` 校验的数据，读取 `knowledge/**/*.md` 的 Front Matter，
生成**只读统计报告**。本脚本**绝不修改任何 Markdown 文件**，也**不写回报告文件**。

## 前置条件

运行前会自动调用 `validate_metadata.py` 的校验逻辑：

- 若存在任意 metadata ERROR：停止生成报告，提示先运行 validator，退出码 `1`
- 仅有 WARNING：仍可生成报告

## 安装依赖

与 `validate_metadata.py` 相同（仅 `PyYAML`）。公共辅助逻辑位于 `metadata_utils.py`，
由以上两个脚本共享。

## 基本运行

```bash
python knowledge/scripts/metadata_report.py
```

输出总览、By Scope / AppCode / Type / Status / Owner / Maintainer / Confidence /
Stability、Evidence Type Usage、Verification Age 分桶，以及交叉统计
AppCode x Type、Status x Confidence。

## 过滤参数

```bash
# 仅统计某个 appCode 的文档（不含 global / cross-app）
python knowledge/scripts/metadata_report.py --app ruoyi-vue-pro

# 仅统计某个知识 type
python knowledge/scripts/metadata_report.py --type tech

# 组合过滤
python knowledge/scripts/metadata_report.py --app ruoyi-vue-pro --type tech
```

`--app` 必须来自 AppCode 注册表，`--type` 必须来自 `builtInTypes + customTypes`，
未知值退出码 `2` 并列出可用值。`--today YYYY-MM-DD` 可覆盖「今天」用于验证年龄分桶。

## 退出码

- `0`：报告生成成功
- `1`：metadata 校验存在 ERROR，报告未生成
- `2`：CLI 参数错误（未知 appCode / type）

