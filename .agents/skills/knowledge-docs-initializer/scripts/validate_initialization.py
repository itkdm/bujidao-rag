#!/usr/bin/env python3
"""校验初始化后的 knowledge/ 与 docs/ 结构。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment failure
    raise SystemExit("缺少 PyYAML，请先执行：python -m pip install pyyaml") from exc


REGISTRY_MARKERS = {
    "appCodes": "APP-CODE",
    "owners": "OWNER",
    "users": "USER",
}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
INDEX_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
REFERENCE_DEFINITION_RE = re.compile(r"^\s*\[(?!\^)[^\]]+\]:\s*(<[^>]+>|\S+)", re.MULTILINE)
PLACEHOLDER_TOKEN_RE = re.compile(r"\{[^{}\r\n]+\}|<[^<>\r\n]+>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", default=".", help="工作区根目录")
    return parser.parse_args()


def is_template(path: Path) -> bool:
    parts = tuple(part.lower() for part in path.parts)
    return (
        parts[:2] == ("knowledge", "template")
        or parts[:3] == ("docs", "changes", "templates")
        or parts[:3] == ("docs", "postmortem", "templates")
    )


def is_raw_reference(relative: Path, filename: str) -> bool:
    return relative.parts[:2] == ("knowledge", "reference") and filename != "README.md"


def without_code_fences(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def front_matter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8-sig")
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", text, re.DOTALL)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else None


def managed_markdown(workspace: Path) -> list[Path]:
    paths: list[Path] = []
    for root_name in ("knowledge", "docs"):
        root = workspace / root_name
        if root.exists():
            paths.extend(path for path in root.rglob("*.md") if path.is_file())
    return sorted(paths)


def template_placeholders(workspace: Path) -> set[str]:
    placeholders: set[str] = {"YYYY-MM-DD"}
    template_roots = (
        workspace / "knowledge" / "template",
        workspace / "docs" / "changes" / "templates",
        workspace / "docs" / "postmortem" / "templates",
    )
    for root in template_roots:
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            placeholders.update(PLACEHOLDER_TOKEN_RE.findall(path.read_text(encoding="utf-8-sig")))
    return placeholders


def extract_registry(text: str, key: str, marker: str) -> list[str]:
    pattern = re.compile(
        rf"<!-- KB-REGISTRY:{marker}:BEGIN -->\s*```yaml\s*(.*?)\s*```\s*"
        rf"<!-- KB-REGISTRY:{marker}:END -->",
        re.DOTALL,
    )
    match = pattern.search(text)
    if not match:
        raise ValueError(f"缺少注册表区块：{marker}")
    data = yaml.safe_load(match.group(1)) or {}
    values = data.get(key)
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise ValueError(f"注册表 {key} 必须是字符串列表")
    return values


def local_target(raw: str) -> str | None:
    target = raw.strip()
    if target.startswith("<") and ">" in target:
        target = target[1 : target.index(">")]
    else:
        target = re.split(r"\s+[\"']", target, maxsplit=1)[0]
    target = unquote(target.split("#", 1)[0]).strip()
    if not target or re.match(r"^(?:https?://|mailto:|tel:|data:)", target, re.IGNORECASE):
        return None
    return target


def is_within_workspace(path: Path, workspace: Path) -> bool:
    try:
        path.relative_to(workspace)
    except ValueError:
        return False
    return True


def validate_links(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_raw_reference(relative, path.name):
            continue
        template_path = is_template(relative)
        if template_path and relative.parts[0] == "knowledge":
            continue
        text = without_code_fences(path.read_text(encoding="utf-8-sig"))
        link_targets = [match.group(1) for match in LINK_RE.finditer(text)]
        link_targets.extend(match.group(1) for match in REFERENCE_DEFINITION_RE.finditer(text))
        for raw_target in link_targets:
            target = local_target(raw_target)
            if target is None:
                continue
            if any(token in target for token in ("{", "}", "<", ">")):
                if not template_path:
                    errors.append(f"链接包含占位符：{relative.as_posix()} -> {raw_target}")
                continue
            target_path = Path(target)
            resolved = (path.parent / target_path).resolve()
            if target_path.is_absolute() or not is_within_workspace(resolved, workspace):
                errors.append(f"链接越出工作区：{relative.as_posix()} -> {raw_target}")
            elif not resolved.exists():
                errors.append(f"链接目标不存在：{relative.as_posix()} -> {raw_target}")


def validate_metadata_refs(
    workspace: Path,
    paths: list[Path],
    registries: dict[str, set[str]],
    errors: list[str],
) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_template(relative) or is_raw_reference(relative, path.name):
            continue
        data = front_matter(path)
        if data is None:
            continue
        app_code = data.get("appCode")
        owner = data.get("owner")
        maintainers = data.get("maintainers", [])
        if app_code is not None and app_code not in registries["appCodes"]:
            errors.append(f"注册表：{relative.as_posix()} 使用了未注册的 appCode {app_code!r}")
        if owner is not None and owner not in registries["owners"]:
            errors.append(f"注册表：{relative.as_posix()} 使用了未注册的 owner {owner!r}")
        for maintainer in maintainers if isinstance(maintainers, list) else []:
            if maintainer not in registries["users"]:
                errors.append(
                    f"注册表：{relative.as_posix()} 使用了未注册的 maintainer {maintainer!r}"
                )
        evidence = data.get("evidence", [])
        if not isinstance(evidence, list):
            continue
        for item in evidence:
            if not isinstance(item, dict) or item.get("type") not in {"code", "doc"}:
                continue
            ref = item.get("ref")
            if not isinstance(ref, str) or not ref or re.match(r"^https?://", ref):
                continue
            if any(token in ref for token in ("{", "}", "<", ">")):
                errors.append(f"证据路径包含占位符：{relative.as_posix()} -> {ref}")
                continue
            ref_path = Path(unquote(ref))
            resolved = (workspace / ref_path).resolve()
            if ref_path.is_absolute() or not is_within_workspace(resolved, workspace):
                errors.append(f"证据路径越出工作区：{relative.as_posix()} -> {ref}")
            elif not resolved.exists():
                errors.append(f"证据路径不存在：{relative.as_posix()} -> {ref}")


def index_targets(index_path: Path) -> set[Path]:
    text = without_code_fences(index_path.read_text(encoding="utf-8-sig"))
    targets: set[Path] = set()
    for match in INDEX_LINK_RE.finditer(text):
        target = local_target(match.group(1))
        if target is not None and "{" not in target and "}" not in target:
            targets.add((index_path.parent / target).resolve())
    return targets


def validate_indexes(workspace: Path, errors: list[str]) -> None:
    knowledge = workspace / "knowledge"
    for index_path in sorted(knowledge.rglob("INDEX.md")):
        relative = index_path.relative_to(workspace)
        if is_template(relative) or "reference" in relative.parts:
            continue
        targets = index_targets(index_path)
        expected: list[Path] = [
            path.resolve()
            for path in index_path.parent.glob("*.md")
            if path.name != "INDEX.md"
        ]
        expected.extend(
            path.resolve()
            for path in index_path.parent.iterdir()
            if path.is_dir() and not path.name.startswith(".")
        )
        allowed: set[Path] = set()
        for item in expected:
            allowed.add(item)
            if item.is_dir() and (item / "INDEX.md").exists():
                allowed.add((item / "INDEX.md").resolve())
        for target in targets:
            if target == index_path.resolve():
                errors.append(f"索引：{relative.as_posix()} 索引了自身")
            elif target not in allowed:
                try:
                    display = target.relative_to(workspace).as_posix()
                except ValueError:
                    display = str(target)
                errors.append(f"索引：{relative.as_posix()} 包含非直接子项 {display}")
        for item in expected:
            candidates = {item}
            if item.is_dir():
                candidates.add((item / "INDEX.md").resolve())
            if targets.isdisjoint(candidates):
                errors.append(
                    f"索引：{relative.as_posix()} 未覆盖 {item.relative_to(workspace).as_posix()}"
                )


def validate_required_layout(workspace: Path, app_codes: set[str], errors: list[str]) -> None:
    required_paths = [
        "knowledge/README.md",
        "knowledge/INDEX.md",
        "knowledge/ROUTING.md",
        "knowledge/KNOWLEDGE-METADATA-RULES.md",
        "knowledge/main",
        "knowledge/applications",
        "knowledge/candidate",
        "knowledge/personal",
        "knowledge/archive",
        "knowledge/reference",
        "knowledge/template",
        "knowledge/scripts",
        "docs/changes/README.md",
        "docs/changes/templates/change.md",
        "docs/changes/templates/design.md",
        "docs/changes/templates/plan.md",
        "docs/changes/templates/research.md",
        "docs/changes/templates/spec.md",
        "docs/postmortem/README.md",
        "docs/postmortem/templates/postmortem.md",
    ]
    for state in ("proposed", "implemented", "rejected", "archived"):
        required_paths.append(f"docs/changes/{state}/README.md")
    for app_code in app_codes:
        app_root = f"knowledge/applications/{app_code}"
        required_paths.extend(
            [f"{app_root}/README.md", f"{app_root}/INDEX.md", f"{app_root}/{app_code}.md"]
        )
        for category in ("base", "feature", "rule", "tech"):
            required_paths.extend(
                [f"{app_root}/{category}/README.md", f"{app_root}/{category}/INDEX.md"]
            )
    for relative in required_paths:
        if not (workspace / relative).exists():
            errors.append(f"目录骨架：缺少 {relative}")


def archived_app_codes(workspace: Path) -> set[str]:
    result: set[str] = set()
    archive = workspace / "knowledge" / "archive"
    if not archive.exists():
        return result
    for path in archive.rglob("*.md"):
        data = front_matter(path)
        if data and isinstance(data.get("appCode"), str):
            result.add(data["appCode"])
    return result


def validate_application_registry(
    workspace: Path, app_codes: set[str], errors: list[str]
) -> set[str]:
    root = workspace / "knowledge" / "applications"
    if not root.exists():
        errors.append("注册表：缺少 knowledge/applications 目录")
        return set()
    directories = {path.name for path in root.iterdir() if path.is_dir()}
    historical = archived_app_codes(workspace)
    orphaned = sorted(app_codes - directories - historical)
    extra = sorted(directories - app_codes)
    if orphaned:
        errors.append(
            "注册表：以下 appCode 既没有当前应用目录，也没有归档引用："
            + ", ".join(orphaned)
        )
    if extra:
        errors.append(f"注册表：存在未注册的应用目录：{', '.join(extra)}")
    return directories


def validate_placeholders(
    workspace: Path, paths: list[Path], placeholders: set[str], errors: list[str]
) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_template(relative):
            continue
        is_application_output = (
            len(relative.parts) >= 4
            and relative.parts[:2] == ("knowledge", "applications")
        )
        is_change_output = (
            len(relative.parts) >= 3
            and relative.parts[:2] == ("docs", "changes")
            and relative.parts[2] in {"proposed", "implemented", "rejected", "archived"}
            and path.name != "README.md"
        )
        is_postmortem_output = (
            len(relative.parts) >= 2
            and relative.parts[:2] == ("docs", "postmortem")
            and path.name != "README.md"
        )
        if not (is_application_output or is_change_output or is_postmortem_output):
            continue
        text = without_code_fences(path.read_text(encoding="utf-8-sig"))
        found = sorted(token for token in placeholders if token in text)
        todo_match = re.search(r"\[TODO\]|TODO:", text, re.IGNORECASE)
        if found:
            errors.append(f"占位符：{relative.as_posix()} 包含 {', '.join(found)}")
        if todo_match:
            errors.append(f"占位符：{relative.as_posix()} 包含 {todo_match.group(0)!r}")


def main() -> int:
    workspace = Path(parse_args().workspace).resolve()
    rules_path = workspace / "knowledge" / "KNOWLEDGE-METADATA-RULES.md"
    if not rules_path.is_file():
        print(f"错误：缺少 {rules_path}")
        return 2

    errors: list[str] = []
    rules_text = rules_path.read_text(encoding="utf-8-sig")
    registries: dict[str, set[str]] = {}
    try:
        for key, marker in REGISTRY_MARKERS.items():
            registries[key] = set(extract_registry(rules_text, key, marker))
    except ValueError as exc:
        print(f"错误：{exc}")
        return 2

    paths = managed_markdown(workspace)
    placeholders = template_placeholders(workspace)
    validate_links(workspace, paths, errors)
    validate_metadata_refs(workspace, paths, registries, errors)
    validate_indexes(workspace, errors)
    active_app_codes = validate_application_registry(workspace, registries["appCodes"], errors)
    validate_required_layout(workspace, active_app_codes, errors)
    validate_placeholders(workspace, paths, placeholders, errors)

    if errors:
        print(f"初始化结构校验失败，共 {len(errors)} 个错误：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "初始化结构校验通过："
        f"发现 {len(paths)} 个 Markdown 文件；目录骨架、链接、证据、索引、注册表和占位符均已检查。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
