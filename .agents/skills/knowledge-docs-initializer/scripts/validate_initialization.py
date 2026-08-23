#!/usr/bin/env python3
"""校验初始化后的 knowledge/ 与 docs/ 轻量目录结构。"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


APP_CODE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONT_MATTER_RE = re.compile(r"\A\ufeff?---\s*\r?\n.*?\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
REFERENCE_DEFINITION_RE = re.compile(r"^\s*\[(?!\^)[^\]]+\]:\s*(<[^>]+>|\S+)", re.MULTILINE)
EVIDENCE_ROW_RE = re.compile(r"^\|\s*(?:code|doc)\s*\|\s*(.*?)\s*\|", re.MULTILINE)
INITIALIZATION_PLACEHOLDER_RE = re.compile(r"\{\{初始化:[^{}\r\n]+\}\}")
FULL_MARKDOWN_LINK_RE = re.compile(r"^\[[^\]\r\n]+\]\((.+)\)$")


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


def is_raw_reference(relative: Path) -> bool:
    return relative.parts[:3] == ("knowledge", "reference", "ruoyi-vue-pro官方文档")


def without_code_fences(text: str, *, strip_inline: bool = True) -> str:
    lines: list[str] = []
    fence_marker: str | None = None
    for line in text.splitlines():
        stripped = line.lstrip()
        marker = stripped[:3] if stripped[:3] in {"```", "~~~"} else None
        if marker and fence_marker is None:
            fence_marker = marker
            continue
        if marker and marker == fence_marker:
            fence_marker = None
            continue
        if fence_marker is None:
            lines.append(line)
    result = "\n".join(lines)
    return re.sub(r"`[^`\r\n]*`", "", result) if strip_inline else result


def managed_markdown(workspace: Path) -> list[Path]:
    paths: list[Path] = []
    for root_name in ("knowledge", "docs"):
        root = workspace / root_name
        if root.exists():
            paths.extend(path for path in root.rglob("*.md") if path.is_file())
    return sorted(paths)


def inline_link_targets(text: str, *, include_images: bool = True) -> list[str]:
    targets: list[str] = []
    cursor = 0
    while True:
        opening = text.find("](", cursor)
        if opening < 0:
            break
        start = opening + 2
        depth = 1
        index = start
        while index < len(text):
            char = text[index]
            if char == "\\":
                index += 2
                continue
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    label_start = text.rfind("[", cursor, opening)
                    label = text[label_start + 1 : opening] if label_start >= 0 else ""
                    is_image = label_start > 0 and text[label_start - 1] == "!"
                    is_escaped = label_start > 0 and text[label_start - 1] == "\\"
                    if (
                        label_start >= 0
                        and "\n" not in label
                        and not is_escaped
                        and (include_images or not is_image)
                    ):
                        targets.append(text[start:index])
                    cursor = index + 1
                    break
            index += 1
        else:
            cursor = start
    return targets


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


def validate_no_frontmatter(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_raw_reference(relative):
            continue
        if FRONT_MATTER_RE.match(path.read_text(encoding="utf-8-sig")):
            errors.append(f"YAML 头：{relative.as_posix()} 不应包含自定义 Front Matter")


def validate_links(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_raw_reference(relative):
            continue
        template_path = is_template(relative)
        if template_path and relative.parts[0] == "knowledge":
            continue
        text = without_code_fences(path.read_text(encoding="utf-8-sig"))
        targets = inline_link_targets(text)
        targets.extend(match.group(1) for match in REFERENCE_DEFINITION_RE.finditer(text))
        for raw_target in targets:
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


def validate_evidence_rows(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_template(relative) or is_raw_reference(relative):
            continue
        text = without_code_fences(
            path.read_text(encoding="utf-8-sig"), strip_inline=False
        )
        is_application_knowledge = (
            len(relative.parts) >= 4
            and relative.parts[:2] == ("knowledge", "applications")
            and path.name not in {"README.md", "INDEX.md"}
        )
        if not is_application_knowledge:
            continue
        heading = re.search(r"^##\s+证据来源\s*$", text, re.MULTILINE)
        if heading is None:
            errors.append(f"证据来源：{relative.as_posix()} 缺少“## 证据来源”章节")
            continue
        section_start = heading.end()
        next_heading = re.search(r"^##\s+", text[section_start:], re.MULTILINE)
        section_end = section_start + next_heading.start() if next_heading else len(text)
        section = text[section_start:section_end]
        rows = list(EVIDENCE_ROW_RE.finditer(section))
        if not rows:
            errors.append(f"证据来源：{relative.as_posix()} 的证据章节没有 code/doc 记录")
            continue
        for match in rows:
            source = match.group(1).strip()
            if not FULL_MARKDOWN_LINK_RE.fullmatch(source):
                errors.append(
                    f"证据来源：{relative.as_posix()} 必须使用完整 Markdown 链接：{source}"
                )


def index_targets(index_path: Path) -> set[Path]:
    text = without_code_fences(index_path.read_text(encoding="utf-8-sig"))
    targets: set[Path] = set()
    for raw_target in inline_link_targets(text, include_images=False):
        target = local_target(raw_target)
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
        expected = [
            path.resolve() for path in index_path.parent.glob("*.md") if path.name != "INDEX.md"
        ]
        expected.extend(
            path.resolve()
            for path in index_path.parent.iterdir()
            if path.is_dir() and not path.name.startswith(".") and any(path.iterdir())
        )
        allowed: set[Path] = set(expected)
        for item in expected:
            if item.is_dir() and (item / "INDEX.md").exists():
                allowed.add((item / "INDEX.md").resolve())
        for target in targets:
            if target == index_path.resolve():
                errors.append(f"索引：{relative.as_posix()} 索引了自身")
            elif target not in allowed:
                display = target.relative_to(workspace).as_posix() if is_within_workspace(target, workspace) else str(target)
                errors.append(f"索引：{relative.as_posix()} 包含非直接子项 {display}")
        for item in expected:
            candidates = {item}
            if item.is_dir():
                candidates.add((item / "INDEX.md").resolve())
            if targets.isdisjoint(candidates):
                errors.append(f"索引：{relative.as_posix()} 未覆盖 {item.relative_to(workspace).as_posix()}")


def application_codes(workspace: Path, errors: list[str]) -> set[str]:
    root = workspace / "knowledge" / "applications"
    if not root.exists():
        errors.append("应用目录：缺少 knowledge/applications")
        return set()
    codes = {path.name for path in root.iterdir() if path.is_dir()}
    for code in sorted(codes):
        if not APP_CODE_RE.fullmatch(code):
            errors.append(f"应用目录：appCode 必须使用小写 kebab-case：{code}")
    return codes


def validate_required_layout(workspace: Path, app_codes: set[str], errors: list[str]) -> None:
    required = [
        "knowledge/README.md",
        "knowledge/INDEX.md",
        "knowledge/ROUTING.md",
        "knowledge/main/README.md",
        "knowledge/main/INDEX.md",
        "knowledge/applications/README.md",
        "knowledge/applications/INDEX.md",
        "knowledge/candidate/README.md",
        "knowledge/candidate/INDEX.md",
        "knowledge/personal/README.md",
        "knowledge/personal/INDEX.md",
        "knowledge/archive/README.md",
        "knowledge/archive/INDEX.md",
        "knowledge/reference/README.md",
        "knowledge/template/common/README-template.md",
        "knowledge/template/common/INDEX-template.md",
        "knowledge/template/applications/{appCode}/application-README-template.md",
        "knowledge/template/applications/{appCode}/application-INDEX-template.md",
        "knowledge/template/applications/{appCode}/application-overview-template.md",
        "knowledge/template/applications/{appCode}/category-INDEX-template.md",
        "knowledge/template/applications/{appCode}/base/README.md",
        "knowledge/template/applications/{appCode}/base/template.md",
        "knowledge/template/applications/{appCode}/feature/README.md",
        "knowledge/template/applications/{appCode}/feature/template.md",
        "knowledge/template/applications/{appCode}/rule/README.md",
        "knowledge/template/applications/{appCode}/rule/template.md",
        "knowledge/template/applications/{appCode}/tech/README.md",
        "knowledge/template/applications/{appCode}/tech/template.md",
        "docs/changes/README.md",
        "docs/changes/templates/change.md",
        "docs/changes/templates/design.md",
        "docs/changes/templates/plan.md",
        "docs/changes/templates/research.md",
        "docs/changes/templates/spec.md",
        "docs/postmortem/README.md",
        "docs/postmortem/templates/postmortem.md",
    ]
    required.extend(f"docs/changes/{state}/README.md" for state in ("proposed", "implemented", "rejected", "archived"))
    for code in app_codes:
        root = f"knowledge/applications/{code}"
        required.extend((f"{root}/README.md", f"{root}/INDEX.md", f"{root}/{code}.md"))
        for category in ("base", "feature", "rule", "tech"):
            required.extend((f"{root}/{category}/README.md", f"{root}/{category}/INDEX.md"))
    for relative in required:
        if not (workspace / relative).exists():
            errors.append(f"目录骨架：缺少 {relative}")


def validate_placeholders(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_template(relative) or is_raw_reference(relative):
            continue
        application_output = len(relative.parts) >= 4 and relative.parts[:2] == ("knowledge", "applications")
        change_output = (
            len(relative.parts) >= 3
            and relative.parts[:2] == ("docs", "changes")
            and relative.parts[2] in {"proposed", "implemented", "rejected", "archived"}
            and path.name != "README.md"
        )
        postmortem_output = relative.parts[:2] == ("docs", "postmortem") and path.name != "README.md"
        text = without_code_fences(
            path.read_text(encoding="utf-8-sig"), strip_inline=False
        )
        found = sorted(set(INITIALIZATION_PLACEHOLDER_RE.findall(text)))
        todo = (
            re.search(r"\[TODO\]|TODO:", text, re.IGNORECASE)
            if application_output or change_output or postmortem_output
            else None
        )
        if found:
            errors.append(f"占位符：{relative.as_posix()} 包含 {', '.join(found)}")
        if todo:
            errors.append(f"占位符：{relative.as_posix()} 包含 {todo.group(0)!r}")


def main() -> int:
    workspace = Path(parse_args().workspace).resolve()
    errors: list[str] = []
    paths = managed_markdown(workspace)
    validate_no_frontmatter(workspace, paths, errors)
    validate_links(workspace, paths, errors)
    validate_evidence_rows(workspace, paths, errors)
    validate_indexes(workspace, errors)
    app_codes = application_codes(workspace, errors)
    validate_required_layout(workspace, app_codes, errors)
    validate_placeholders(workspace, paths, errors)

    if errors:
        print(f"初始化结构校验失败，共 {len(errors)} 个错误：")
        for error in errors:
            print(f"- {error}")
        return 1

    raw_count = sum(is_raw_reference(path.relative_to(workspace)) for path in paths)
    managed_count = len(paths) - raw_count
    print(
        "初始化结构校验通过："
        f"已检查 {managed_count} 个受管理 Markdown 文件，跳过 {raw_count} 个原始导入参考文件；"
        "YAML 头、目录骨架、链接、正文证据、应用目录、索引和占位符均已检查。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
