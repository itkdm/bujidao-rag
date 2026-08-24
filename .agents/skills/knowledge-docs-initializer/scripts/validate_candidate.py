#!/usr/bin/env python3
"""校验 candidate/ 的目标镜像、正文契约和受管理目录。"""

from __future__ import annotations

import re
from pathlib import Path


APP_CODE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CANDIDATE_ROOTS = {"main", "applications"}
OPTIONAL_CANDIDATE_ROOTS = {"unclassified"}
APPLICATION_CATEGORIES = {"base", "feature", "rule", "tech"}
INFRASTRUCTURE_FILES = {"README.md", "INDEX.md"}
FORBIDDEN_STATE_DIRECTORIES = {"pending", "reviewed", "approved"}
REQUIRED_HEADINGS = (
    "候选结论",
    "拟晋升位置",
    "为什么仍是候选",
    "证据",
    "待确认问题",
    "验证与晋升条件",
)
TARGET_RE = re.compile(
    r"`(knowledge/(?:main|applications)/[^`\r\n]+\.md)`"
)
TITLE_RE = re.compile(r"^#(?!#)\s+\S.*$", re.MULTILINE)


def markdown_without_code_fences(text: str) -> str:
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
    return "\n".join(lines)


def section_body(text: str, heading: str) -> str | None:
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if match is None:
        return None
    start = match.end()
    next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(text)
    return text[start:end].strip()


def expected_target(relative: Path) -> str | None:
    if relative.parts[0] not in CANDIDATE_ROOTS:
        return None
    return Path("knowledge", *relative.parts).as_posix()


def validate_candidate_path(relative: Path, errors: list[str]) -> None:
    display = Path("knowledge/candidate", relative).as_posix()
    root_name = relative.parts[0]
    if root_name == "applications":
        if len(relative.parts) < 3:
            errors.append(
                f"候选路径：{display} 必须位于 applications/<appCode>/ 下"
            )
            return
        app_code = relative.parts[1]
        if not APP_CODE_RE.fullmatch(app_code):
            errors.append(
                f"候选路径：{display} 的 appCode 必须使用小写 kebab-case"
            )
        if len(relative.parts) >= 4 and relative.parts[2] not in APPLICATION_CATEGORIES:
            errors.append(
                f"候选路径：{display} 的应用分类必须是 "
                "base、feature、rule 或 tech"
            )


def validate_candidate_file(path: Path, root: Path, errors: list[str]) -> None:
    relative = path.relative_to(root)
    display = Path("knowledge/candidate", relative).as_posix()
    if len(relative.parts) < 2:
        errors.append(f"候选路径：候选正文不能直接放在 candidate 根目录：{display}")
        return
    if relative.parts[0] not in CANDIDATE_ROOTS | OPTIONAL_CANDIDATE_ROOTS:
        errors.append(f"候选路径：{display} 不属于允许的候选目标域")
        return

    validate_candidate_path(relative, errors)
    text = markdown_without_code_fences(path.read_text(encoding="utf-8-sig"))
    sections = validate_candidate_body(text, display, errors)

    target_section = sections.get("拟晋升位置", "")
    targets = TARGET_RE.findall(target_section)
    if relative.parts[0] == "unclassified":
        if targets or "待分类" not in target_section:
            errors.append(
                f"候选目标：{display} 位于 unclassified 时必须写“待分类”，"
                "不能伪造正式路径"
            )
        return

    expected = expected_target(relative)
    if targets != [expected]:
        errors.append(
            f"候选目标：{display} 的拟晋升位置必须且只能是 `{expected}`"
        )


def validate_candidate_body(
    text: str, display: str, errors: list[str]
) -> dict[str, str]:
    """校验候选正文的通用结构，并返回已成功识别的章节。"""
    titles = TITLE_RE.findall(text)
    if len(titles) != 1:
        errors.append(f"候选正文：{display} 必须且只能包含一个非空一级标题")
    positions: list[int] = []
    sections: dict[str, str] = {}
    for heading in REQUIRED_HEADINGS:
        matches = list(
            re.finditer(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
        )
        if len(matches) != 1:
            errors.append(
                f"候选正文：{display} 必须且只能包含一个“## {heading}”章节"
            )
            continue
        positions.append(matches[0].start())
        sections[heading] = section_body(text, heading) or ""
    if len(positions) == len(REQUIRED_HEADINGS) and positions != sorted(positions):
        errors.append(f"候选正文：{display} 的必需章节顺序不符合候选模板")
    for heading, body in sections.items():
        if not body:
            errors.append(f"候选正文：{display} 的“{heading}”章节不能为空")
    return sections


def validate_candidate_layout(workspace: Path, errors: list[str]) -> None:
    root = workspace / "knowledge" / "candidate"
    if not root.is_dir():
        errors.append("候选结构：缺少 knowledge/candidate")
        return

    direct_directories = {
        path.name
        for path in root.iterdir()
        if path.is_dir() and not path.name.startswith(".")
    }
    missing = sorted(CANDIDATE_ROOTS - direct_directories)
    unexpected = sorted(
        direct_directories - CANDIDATE_ROOTS - OPTIONAL_CANDIDATE_ROOTS
    )
    if missing:
        errors.append(f"候选结构：缺少候选目标域：{', '.join(missing)}")
    if unexpected:
        errors.append(f"候选结构：存在未知候选目标域：{', '.join(unexpected)}")

    candidate_applications = root / "applications"
    formal_applications = workspace / "knowledge" / "applications"
    if candidate_applications.is_dir():
        for app_directory in sorted(
            path for path in candidate_applications.iterdir() if path.is_dir()
        ):
            app_code = app_directory.name
            if not APP_CODE_RE.fullmatch(app_code):
                errors.append(
                    "候选结构：candidate/applications 下的 appCode 必须使用"
                    f"小写 kebab-case：{app_code}"
                )
            if not (formal_applications / app_code).is_dir():
                errors.append(
                    "候选结构：未确认的应用边界应进入 unclassified，"
                    f"正式 applications 中不存在 appCode：{app_code}"
                )
            for category in sorted(
                path for path in app_directory.iterdir() if path.is_dir()
            ):
                if category.name not in APPLICATION_CATEGORIES:
                    errors.append(
                        f"候选结构：{category.relative_to(workspace).as_posix()} "
                        "必须使用 base、feature、rule 或 tech 分类"
                    )

    for directory in sorted(path for path in root.rglob("*") if path.is_dir()):
        relative_parts = directory.relative_to(root).parts
        forbidden_parts = sorted(
            part
            for part in relative_parts
            if part.casefold() in FORBIDDEN_STATE_DIRECTORIES
        )
        if forbidden_parts:
            relative = directory.relative_to(workspace).as_posix()
            errors.append(
                f"候选结构：{relative} 使用了状态目录："
                f"{', '.join(forbidden_parts)}；候选状态不得编码进目录"
            )
        for infrastructure in INFRASTRUCTURE_FILES:
            if not (directory / infrastructure).is_file():
                relative = directory.relative_to(workspace).as_posix()
                errors.append(f"候选结构：{relative} 缺少 {infrastructure}")
        if directory.name not in CANDIDATE_ROOTS or directory.parent != root:
            has_candidate_content = any(
                path.is_file()
                and path.suffix.lower() == ".md"
                and path.name not in INFRASTRUCTURE_FILES
                for path in directory.rglob("*")
            )
            if not has_candidate_content:
                relative = directory.relative_to(workspace).as_posix()
                errors.append(
                    f"候选结构：{relative} 没有候选正文，不应预造空候选目录"
                )

    for path in sorted(path for path in root.rglob("*") if path.is_file()):
        if path.suffix.lower() != ".md":
            relative = path.relative_to(workspace).as_posix()
            errors.append(
                f"候选结构：{relative} 不是 Markdown；原始资料和附件应进入 reference"
            )

    for path in sorted(root.rglob("*.md")):
        if path.name in INFRASTRUCTURE_FILES:
            text = markdown_without_code_fences(
                path.read_text(encoding="utf-8-sig")
            )
            if any(
                re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
                for heading in REQUIRED_HEADINGS
            ):
                display = path.relative_to(workspace).as_posix()
                errors.append(
                    f"候选结构：{display} 是导航基础设施，不能承载候选正文"
                )
        else:
            validate_candidate_file(path, root, errors)

    template = workspace / "knowledge" / "template" / "candidate" / "candidate.md"
    if template.is_file():
        text = markdown_without_code_fences(
            template.read_text(encoding="utf-8-sig")
        )
        validate_candidate_body(
            text,
            "knowledge/template/candidate/candidate.md",
            errors,
        )
