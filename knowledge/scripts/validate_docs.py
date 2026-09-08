#!/usr/bin/env python3
"""校验 Change 与 Postmortem 实例的目录、命名和必选正文结构。"""

from __future__ import annotations

import re
from collections import defaultdict
from datetime import date
from pathlib import Path


CHANGE_STATES = {"proposed", "implemented", "rejected", "archived"}
CHANGE_TYPES = {
    "feature",
    "bug-fix",
    "architecture",
    "simplification",
    "process",
    "testing",
}
CHANGE_FILES = {"change.md", "spec.md", "research.md", "design.md", "plan.md"}
DATED_SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")
POSTMORTEM_FILE_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*\.md$"
)
BASE_CHANGE_HEADINGS = ("概要", "问题", "目标与范围")
POSTMORTEM_HEADINGS = (
    "执行摘要",
    "影响与发生了什么",
    "根因",
    "为什么逃过防线",
    "防线（Guardrails）",
)


def markdown_sections(path: Path) -> dict[tuple[int, str], list[list[str]]]:
    """读取 CommonMark 风格 ATX 标题及其正文，忽略围栏与 HTML 注释。"""
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    sections: dict[tuple[int, str], list[list[str]]] = defaultdict(list)
    active: dict[int, list[str]] = {}
    opening: tuple[str, int] | None = None

    for line in text.splitlines():
        if opening is not None:
            closing = re.match(r"^ {0,3}([`~]+)[ \t]*$", line)
            if (
                closing
                and closing.group(1)[0] == opening[0]
                and len(closing.group(1)) >= opening[1]
            ):
                opening = None
            continue

        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            opening = (fence.group(1)[0], len(fence.group(1)))
            continue

        heading = re.match(r"^ {0,3}(#{1,6})(?:[ \t]+|$)(.*)$", line)
        if heading:
            level = len(heading.group(1))
            title = re.sub(r"[ \t]+#+[ \t]*$", "", heading.group(2)).strip()
            body: list[str] = []
            sections[(level, title)].append(body)
            active = {key: value for key, value in active.items() if key < level}
            active[level] = body
            continue

        stripped = line.strip()
        for body in active.values():
            body.append(stripped)

    return dict(sections)


def has_meaningful_content(lines: list[str]) -> bool:
    return any(re.search(r"[0-9A-Za-z\u4e00-\u9fff]", line) for line in lines)


def require_section(
    sections: dict[tuple[int, str], list[list[str]]],
    *,
    level: int,
    title: str,
    kind: str,
    relative: str,
    errors: list[str],
) -> None:
    matches = sections.get((level, title), [])
    label = "二级" if level == 2 else "三级"
    if not matches:
        errors.append(f"{kind} 结构：{relative} 缺少{label}标题“{title}”")
        return
    if len(matches) > 1:
        errors.append(f"{kind} 结构：{relative} 重复{label}标题“{title}”")
    if not any(has_meaningful_content(body) for body in matches):
        errors.append(f"{kind} 结构：{relative} 的{label}章节“{title}”不能为空")


def valid_dated_slug(value: str) -> bool:
    if not DATED_SLUG_RE.fullmatch(value):
        return False
    try:
        date.fromisoformat(value[:10])
    except ValueError:
        return False
    return True


def validate_change_document(
    workspace: Path, path: Path, state: str, errors: list[str]
) -> None:
    relative = path.relative_to(workspace).as_posix()
    sections = markdown_sections(path)
    for heading in BASE_CHANGE_HEADINGS:
        require_section(
            sections,
            level=2,
            title=heading,
            kind="Change",
            relative=relative,
            errors=errors,
        )

    state_required = {
        "proposed": ("方案", "验收标准"),
        "implemented": ("最终决策", "验证结果"),
        "rejected": ("方案", "验收标准"),
        "archived": ("最终决策", "验证结果"),
    }
    for heading in state_required.get(state, ()):
        require_section(
            sections,
            level=2,
            title=heading,
            kind="Change",
            relative=relative,
            errors=errors,
        )

    if state in {"implemented", "archived"}:
        for old_heading, new_heading in (
            ("方案", "最终决策"),
            ("验收标准", "验证结果"),
        ):
            if (2, old_heading) in sections:
                errors.append(
                    f"Change 结构：{relative} 已进入 {state}，必须将“{old_heading}”转换为“{new_heading}”"
                )

    if state == "rejected":
        for level, title in ((2, "拒绝状态补充"), (3, "拒绝原因")):
            require_section(
                sections,
                level=level,
                title=title,
                kind="Change",
                relative=relative,
                errors=errors,
            )
    if state == "archived":
        for level, title in ((2, "归档状态补充"), (3, "归档原因")):
            require_section(
                sections,
                level=level,
                title=title,
                kind="Change",
                relative=relative,
                errors=errors,
            )


def validate_changes(workspace: Path, errors: list[str]) -> None:
    root = workspace / "docs" / "changes"
    if not root.is_dir():
        return

    allowed_root_entries = CHANGE_STATES | {"README.md", "templates"}
    for entry in root.iterdir():
        if entry.name not in allowed_root_entries:
            errors.append(f"Change 目录：docs/changes/ 存在未定义子项 {entry.name}")

    identities: dict[str, list[str]] = defaultdict(list)
    for state in sorted(CHANGE_STATES):
        state_root = root / state
        if not state_root.is_dir():
            errors.append(f"Change 目录：缺少 docs/changes/{state}/")
            continue
        for entry in state_root.iterdir():
            if entry.name == "README.md" and entry.is_file():
                continue
            if not entry.is_dir():
                errors.append(
                    f"Change 目录：docs/changes/{state}/ 只能直接包含 README.md 与类型目录：{entry.name}"
                )
                continue
            if entry.name not in CHANGE_TYPES:
                errors.append(
                    f"Change 目录：docs/changes/{state}/ 存在未定义类型 {entry.name}"
                )
                continue
            for change_dir in entry.iterdir():
                relative = change_dir.relative_to(workspace).as_posix()
                if not change_dir.is_dir():
                    errors.append(f"Change 目录：{relative} 必须位于独立 Change 目录中")
                    continue
                identities[change_dir.name].append(relative)
                if not valid_dated_slug(change_dir.name):
                    errors.append(f"Change 命名：{relative} 必须使用 YYYY-MM-DD-kebab-slug")
                change_file = change_dir / "change.md"
                if not change_file.is_file():
                    errors.append(f"Change 结构：{relative} 缺少 change.md")
                else:
                    validate_change_document(workspace, change_file, state, errors)
                for child in change_dir.iterdir():
                    child_relative = child.relative_to(workspace).as_posix()
                    if child.is_dir() or child.name not in CHANGE_FILES:
                        errors.append(
                            f"Change 结构：{child_relative} 不是允许的 Change 文档"
                        )

    for identity, locations in sorted(identities.items()):
        if len(locations) > 1:
            errors.append(
                "Change 身份：同一 YYYY-MM-DD-slug 只能存在一次："
                f"{identity} -> {', '.join(sorted(locations))}"
            )


def validate_postmortems(workspace: Path, errors: list[str]) -> None:
    root = workspace / "docs" / "postmortem"
    if not root.is_dir():
        return
    for entry in root.iterdir():
        relative = entry.relative_to(workspace).as_posix()
        if entry.name == "README.md" and entry.is_file():
            continue
        if entry.name == "templates" and entry.is_dir():
            continue
        dated_slug = entry.name.removesuffix(".md")
        if (
            not entry.is_file()
            or not POSTMORTEM_FILE_RE.fullmatch(entry.name)
            or not valid_dated_slug(dated_slug)
        ):
            errors.append(
                f"Postmortem 命名：{relative} 必须是 docs/postmortem/YYYY-MM-DD-kebab-slug.md"
            )
            continue
        sections = markdown_sections(entry)
        for heading in POSTMORTEM_HEADINGS:
            require_section(
                sections,
                level=2,
                title=heading,
                kind="Postmortem",
                relative=relative,
                errors=errors,
            )
        for heading in ("测试", "评审", "工具 / CI", "流程 / 规范"):
            require_section(
                sections,
                level=3,
                title=heading,
                kind="Postmortem",
                relative=relative,
                errors=errors,
            )


def validate_docs_layout(workspace: Path, errors: list[str]) -> None:
    validate_changes(workspace, errors)
    validate_postmortems(workspace, errors)
