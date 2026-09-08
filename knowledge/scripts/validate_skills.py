#!/usr/bin/env python3
"""校验模板配套项目 Skill 的最小自包含结构，不依赖 YAML 第三方库。"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import NamedTuple


PROJECT_SKILLS = (
    "knowledge-docs-initializer",
    "knowledge-docs-maintenance",
    "knowledge-driven-development",
)
SKILL_ROOTS = (Path(".agent/skills"), Path(".agents/skills"))
SKILL_TOP_LEVEL_KEYS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
}
OPENAI_TOP_LEVEL_KEYS = {"interface", "policy", "dependencies"}
INTERFACE_KEYS = {
    "display_name",
    "short_description",
    "default_prompt",
    "icon_small",
    "icon_large",
    "brand_color",
}


class YamlToken(NamedTuple):
    indent: int
    is_list: bool
    key: str | None
    value: str | None
    raw_value: str | None
    line_number: int


def parse_yaml_scalar(raw: str) -> str | None:
    value = raw.strip()
    if not value:
        return None
    if value.startswith(("[", "{")):
        try:
            json.loads(value)
        except json.JSONDecodeError:
            return None
        return value
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return None
        return parsed if isinstance(parsed, str) else None
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            return None
        inner = value[1:-1]
        if "'" in inner.replace("''", ""):
            return None
        return inner.replace("''", "'")
    if (
        value[0] in "?:,#&*!|>@`"
        or value.endswith(("'", '"'))
        or re.search(r":\s|\s#", value)
    ):
        return None
    return value


def is_yaml_string(raw: str | None, *, require_double_quotes: bool) -> bool:
    if raw is None:
        return False
    value = raw.strip()
    if require_double_quotes:
        if not value.startswith('"'):
            return False
        try:
            return isinstance(json.loads(value), str)
        except json.JSONDecodeError:
            return False
    if value.startswith(("[", "{")):
        return False
    if value.startswith(('"', "'")):
        return parse_yaml_scalar(value) is not None
    lowered = value.lower()
    if lowered in {
        "null",
        "~",
        "true",
        "false",
        "yes",
        "no",
        "on",
        "off",
        ".nan",
        ".inf",
        "+.inf",
        "-.inf",
    }:
        return False
    if re.fullmatch(
        r"[+-]?(?:0[xob][0-9a-f_]+|\d[\d_]*(?:\.\d[\d_]*)?(?:e[+-]?\d+)?|\.\d+(?:e[+-]?\d+)?)",
        lowered,
    ):
        return False
    if re.fullmatch(r"[1-9][0-9_]*(?::[0-5]?[0-9])+(?:\.[0-9_]*)?", value):
        return False
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}(?:[Tt ].*)?", value):
        return False
    return parse_yaml_scalar(value) is not None


def parse_yaml_subset(
    lines: list[str],
    *,
    allowed_top_level: set[str],
    relative: str,
    errors: list[str],
) -> list[YamlToken]:
    tokens: list[YamlToken] = []
    levels = [0]
    previous_can_nest = False
    valid = True
    top_level_seen: set[str] = set()
    parent_at_indent: dict[int, int] = {0: -1}
    collection_types: dict[tuple[int, int], str] = {}

    for line_number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\t" in line[: len(line) - len(line.lstrip())]:
            valid = False
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent % 2:
            valid = False
            continue
        if not tokens and indent != 0:
            valid = False
            continue
        if tokens:
            if indent > levels[-1]:
                if indent != levels[-1] + 2 or not previous_can_nest:
                    valid = False
                    continue
                levels.append(indent)
                parent_at_indent[indent] = len(tokens) - 1
            elif indent < levels[-1]:
                while levels and indent < levels[-1]:
                    levels.pop()
                if not levels or indent != levels[-1]:
                    valid = False
                    continue

        content = line[indent:]
        is_list = content.startswith("- ")
        if is_list:
            content = content[2:].strip()
            if not content:
                valid = False
                continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_-]*):(?:\s+(.+))?", content)
        if match:
            key = match.group(1)
            raw_value = match.group(2)
            value = None if raw_value is None else parse_yaml_scalar(raw_value)
            if raw_value is not None and value is None:
                valid = False
                continue
        elif is_list:
            key = None
            value = parse_yaml_scalar(content)
            if value is None:
                valid = False
                continue
        else:
            valid = False
            continue

        if indent == 0:
            if is_list or key not in allowed_top_level or key in top_level_seen:
                valid = False
                continue
            top_level_seen.add(key)
        parent_id = parent_at_indent.get(indent, -1)
        collection_key = (parent_id, indent)
        collection_type = "sequence" if is_list else "mapping"
        existing_type = collection_types.get(collection_key)
        if existing_type is not None and existing_type != collection_type:
            valid = False
            continue
        collection_types[collection_key] = collection_type
        token = YamlToken(indent, is_list, key, value, raw_value, line_number)
        tokens.append(token)
        previous_can_nest = value is None or (is_list and key is not None)

    if not valid:
        errors.append(f"Skill 结构：{relative} 不是受支持的有效 YAML 结构")
    return tokens


def parse_skill_frontmatter(
    lines: list[str], relative: str, errors: list[str]
) -> dict[str, str]:
    tokens = parse_yaml_subset(
        lines,
        allowed_top_level=SKILL_TOP_LEVEL_KEYS,
        relative=relative,
        errors=errors,
    )
    values: dict[str, str] = {}
    valid = True
    for token in tokens:
        if token.indent != 0 or token.key not in {"name", "description"}:
            continue
        if (
            token.key in values
            or token.value is None
            or not is_yaml_string(token.raw_value, require_double_quotes=False)
        ):
            valid = False
            continue
        values[token.key] = token.value
    if not valid or set(values) != {"name", "description"}:
        errors.append(
            f"Skill 结构：{relative} 的 YAML 头必须包含唯一且有效的 name 与 description"
        )
    return values


def parse_interface_yaml(
    text: str, relative: str, errors: list[str]
) -> dict[str, str]:
    tokens = parse_yaml_subset(
        text.splitlines(),
        allowed_top_level=OPENAI_TOP_LEVEL_KEYS,
        relative=relative,
        errors=errors,
    )
    interface_indexes = [
        index
        for index, token in enumerate(tokens)
        if token.indent == 0 and token.key == "interface" and token.value is None
    ]
    if len(interface_indexes) != 1:
        errors.append(f"Skill 结构：{relative} 必须包含唯一的 interface 根节点")
        return {}
    start = interface_indexes[0] + 1
    values: dict[str, str] = {}
    valid = True
    for token in tokens[start:]:
        if token.indent == 0:
            break
        if token.indent != 2:
            continue
        if (
            token.is_list
            or token.key not in INTERFACE_KEYS
            or token.value is None
            or not is_yaml_string(token.raw_value, require_double_quotes=True)
        ):
            valid = False
            continue
        if token.key not in {"display_name", "short_description", "default_prompt"}:
            continue
        if token.key in values:
            valid = False
            continue
        values[token.key] = token.value
    required = {"display_name", "short_description", "default_prompt"}
    if not valid or set(values) != required:
        errors.append(
            f"Skill 结构：{relative} 的 interface 必须包含唯一且有效的 display_name、short_description、default_prompt"
        )
    return values


def validate_skill_dir(workspace: Path, skill_dir: Path, errors: list[str]) -> None:
    relative_dir = skill_dir.relative_to(workspace).as_posix()
    expected_name = skill_dir.name
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        errors.append(f"Skill 结构：{relative_dir}/ 缺少 SKILL.md")
        return

    text = skill_file.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"Skill 结构：{relative_dir}/SKILL.md 缺少 YAML 头起始分隔符")
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append(f"Skill 结构：{relative_dir}/SKILL.md 缺少 YAML 头结束分隔符")
        return

    frontmatter = parse_skill_frontmatter(
        lines[1:end], f"{relative_dir}/SKILL.md", errors
    )
    name = frontmatter.get("name")
    description = frontmatter.get("description")
    if name != expected_name:
        errors.append(
            f"Skill 结构：{relative_dir}/SKILL.md 的 name 必须等于目录名 {expected_name}"
        )
    if not description or len(description) > 1024:
        errors.append(
            f"Skill 结构：{relative_dir}/SKILL.md 的 description 必须为 1 到 1024 个字符"
        )
    if not any(line.strip() for line in lines[end + 1 :]):
        errors.append(f"Skill 结构：{relative_dir}/SKILL.md 缺少正文")

    ui_file = skill_dir / "agents" / "openai.yaml"
    if not ui_file.is_file():
        errors.append(f"Skill 结构：{relative_dir}/ 缺少 agents/openai.yaml")
        return
    ui_text = ui_file.read_text(encoding="utf-8-sig")
    ui_values = parse_interface_yaml(
        ui_text, f"{relative_dir}/agents/openai.yaml", errors
    )
    display_name = ui_values.get("display_name")
    short_description = ui_values.get("short_description")
    default_prompt = ui_values.get("default_prompt")
    if not display_name:
        errors.append(f"Skill 结构：{relative_dir}/agents/openai.yaml 缺少 display_name")
    if not short_description or not 25 <= len(short_description) <= 64:
        errors.append(
            f"Skill 结构：{relative_dir}/agents/openai.yaml 的 short_description 必须为 25 到 64 个字符"
        )
    if not default_prompt or f"${expected_name}" not in default_prompt:
        errors.append(
            f"Skill 结构：{relative_dir}/agents/openai.yaml 的 default_prompt 必须引用 ${expected_name}"
        )


def validate_project_skills(workspace: Path, errors: list[str]) -> None:
    agents_path = workspace / "AGENTS.md"
    agents_text = (
        agents_path.read_text(encoding="utf-8-sig") if agents_path.is_file() else ""
    )
    knowledge_readme = workspace / "knowledge" / "README.md"
    if knowledge_readme.is_file():
        agents_text += knowledge_readme.read_text(encoding="utf-8-sig")
    agents_template = workspace / "knowledge" / "template" / "common" / "AGENTS-template.md"
    if agents_template.is_file():
        agents_text += agents_template.read_text(encoding="utf-8-sig")
    agents_requires_skills = any(
        name in agents_text
        for name in ("knowledge-docs-maintenance", "knowledge-driven-development")
    )

    populated_roots: list[Path] = []
    for relative_root in SKILL_ROOTS:
        root = workspace / relative_root
        if any((root / name).exists() for name in PROJECT_SKILLS):
            populated_roots.append(root)

    if len(populated_roots) > 1:
        roots = ", ".join(root.relative_to(workspace).as_posix() for root in populated_roots)
        errors.append(f"Skill 结构：三个配套 Skill 不能分散在多个项目 Skill 根目录：{roots}")
        return

    if populated_roots:
        root = populated_roots[0]
    else:
        active_roots = [
            workspace / relative_root
            for relative_root in SKILL_ROOTS
            if (workspace / relative_root).is_dir()
            and any(
                child.is_dir() and (child / "SKILL.md").is_file()
                for child in (workspace / relative_root).iterdir()
            )
        ]
        if not agents_requires_skills and not active_roots:
            return
        if len(active_roots) > 1:
            roots = ", ".join(
                item.relative_to(workspace).as_posix() for item in active_roots
            )
            errors.append(f"Skill 结构：无法确定配套 Skill 的唯一项目根目录：{roots}")
            return
        if not active_roots:
            errors.append(
                "Skill 结构：AGENTS 仍要求使用日常项目 Skill，但 .agent/skills/ 与 .agents/skills/ 中均未交付"
            )
            return
        root = active_roots[0]

    for name in PROJECT_SKILLS:
        skill_dir = root / name
        if not skill_dir.is_dir():
            errors.append(
                "Skill 结构：宿主支持项目 Skill 时必须同时交付 initializer 和两个日常 Skill："
                f"缺少 {skill_dir.relative_to(workspace).as_posix()}/"
            )
            continue
        validate_skill_dir(workspace, skill_dir, errors)
