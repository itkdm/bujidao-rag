# proposed

讨论中、准备实施或正在实施的 Change 放在本目录。

按类型再分子目录（实际产生时创建）：

```text
proposed/
├── feature/
├── bug-fix/
├── architecture/
├── simplification/
├── process/
└── testing/
```

每个 Change 目录命名：`<YYYY-MM-DD>-<slug>/`，至少包含 `change.md`。
实现完成后移至 `../implemented/`；若拒绝则移至 `../rejected/`。
