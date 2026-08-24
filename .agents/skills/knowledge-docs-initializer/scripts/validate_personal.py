#!/usr/bin/env python3
"""校验 personal/ 的所有者边界、导航基础设施和稳定标识。"""

from __future__ import annotations

import re
from pathlib import Path


OWNER_CODE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
OWNER_CODE_LINE_RE = re.compile(
    r"^\s*[-*+]\s+稳定标识：\s*`([^`\r\n]+)`\s*$", re.MULTILINE
)
DISPLAY_NAME_LINE_RE = re.compile(
    r"^\s*[-*+]\s+显示名称：\s*(\S.*?)\s*$", re.MULTILINE
)
INFRASTRUCTURE_FILES = {"README.md", "INDEX.md"}


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


def validate_owner_readme(
    path: Path,
    owner_code: str,
    display: str,
    errors: list[str],
) -> None:
    text = markdown_without_code_fences(path.read_text(encoding="utf-8-sig"))
    identifiers = OWNER_CODE_LINE_RE.findall(text)
    if identifiers != [owner_code]:
        errors.append(
            f"个人知识：{display} 必须且只能声明一个与目录一致的"
            f"稳定标识 `{owner_code}`"
        )
    display_names = DISPLAY_NAME_LINE_RE.findall(text)
    if len(display_names) != 1:
        errors.append(
            f"个人知识：{display} 必须且只能声明一个非空显示名称"
        )


def validate_personal_template(workspace: Path, errors: list[str]) -> None:
    template = (
        workspace
        / "knowledge"
        / "template"
        / "personal"
        / "{ownerCode}"
        / "README.md"
    )
    if not template.is_file():
        return
    text = markdown_without_code_fences(template.read_text(encoding="utf-8-sig"))
    expected = "- 稳定标识：`{{初始化:ownerCode}}`"
    if text.count(expected) != 1:
        errors.append(
            "个人模板：knowledge/template/personal/{ownerCode}/README.md "
            "必须且只能声明一次稳定 ownerCode 占位符"
        )
    title_placeholder = "# {{初始化:显示名称}}的个人知识"
    if text.count(title_placeholder) != 1:
        errors.append(
            "个人模板：knowledge/template/personal/{ownerCode}/README.md "
            "必须且只能包含一个显示名称标题占位符"
        )
    display_name_placeholder = (
        "- 显示名称：{{初始化:姓名、昵称或团队内称呼}}"
    )
    if text.count(display_name_placeholder) != 1:
        errors.append(
            "个人模板：knowledge/template/personal/{ownerCode}/README.md "
            "必须且只能包含一个显示名称声明占位符"
        )

    index_template = template.with_name("INDEX.md")
    if not index_template.is_file():
        return
    index_text = markdown_without_code_fences(
        index_template.read_text(encoding="utf-8-sig")
    )
    required_fragments = {
        "ownerCode 标题占位符": "# {{初始化:ownerCode}}/ 索引",
        "README 导航链接": "[`README.md`](./README.md)",
        "个人内容说明占位符": "{{初始化:个人内容说明}}",
    }
    for label, fragment in required_fragments.items():
        if index_text.count(fragment) != 1:
            errors.append(
                "个人模板：knowledge/template/personal/{ownerCode}/INDEX.md "
                f"必须且只能包含一个{label}"
            )
    if index_text.count("{{初始化:个人内容文件}}") != 2:
        errors.append(
            "个人模板：knowledge/template/personal/{ownerCode}/INDEX.md "
            "必须使用同一个个人内容文件占位符组成链接"
        )


def validate_personal_layout(workspace: Path, errors: list[str]) -> None:
    root = workspace / "knowledge" / "personal"
    if not root.is_dir():
        errors.append("个人知识结构：缺少 knowledge/personal")
        return

    unexpected_root_files = sorted(
        path.name
        for path in root.iterdir()
        if path.is_file() and path.name not in INFRASTRUCTURE_FILES
    )
    if unexpected_root_files:
        errors.append(
            "个人知识结构：个人内容不能直接放在 personal 根目录："
            + ", ".join(unexpected_root_files)
        )

    for owner_directory in sorted(
        path for path in root.iterdir() if path.is_dir()
    ):
        owner_code = owner_directory.name
        relative_owner = owner_directory.relative_to(workspace).as_posix()
        if not OWNER_CODE_RE.fullmatch(owner_code):
            errors.append(
                f"个人知识结构：{relative_owner} 的 ownerCode 必须使用"
                "小写 kebab-case"
            )

        owner_readme = owner_directory / "README.md"
        if owner_readme.is_file():
            validate_owner_readme(
                owner_readme,
                owner_code,
                owner_readme.relative_to(workspace).as_posix(),
                errors,
            )

        has_personal_content = any(
            path.is_file()
            and path.suffix.lower() == ".md"
            and path.name not in INFRASTRUCTURE_FILES
            for path in owner_directory.rglob("*")
        )
        if not has_personal_content:
            errors.append(
                f"个人知识结构：{relative_owner} 没有个人内容，"
                "不应预造空所有者目录"
            )

        for directory in sorted(
            path
            for path in owner_directory.rglob("*")
            if path.is_dir()
        ):
            nested_has_content = any(
                path.is_file()
                and path.suffix.lower() == ".md"
                and path.name not in INFRASTRUCTURE_FILES
                for path in directory.rglob("*")
            )
            if not nested_has_content:
                relative = directory.relative_to(workspace).as_posix()
                errors.append(
                    f"个人知识结构：{relative} 没有个人内容，"
                    "不应预造空主题目录"
                )

    for directory in sorted(path for path in root.rglob("*") if path.is_dir()):
        relative = directory.relative_to(workspace).as_posix()
        for infrastructure in INFRASTRUCTURE_FILES:
            if not (directory / infrastructure).is_file():
                errors.append(f"个人知识结构：{relative} 缺少 {infrastructure}")

    validate_personal_template(workspace, errors)
