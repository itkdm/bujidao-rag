#!/usr/bin/env python3
"""校验当前工作区的 AGENTS、knowledge 与 docs 轻量目录结构。"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

from validate_candidate import validate_candidate_layout
from validate_docs import validate_docs_layout
from validate_personal import validate_personal_layout
from validate_skills import validate_project_skills


for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8")


APP_CODE_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
APP_CODE_ROW_RE = re.compile(
    r"^\|\s*应用编码\s*\|\s*`?([^`|\s]+)`?\s*\|", re.MULTILINE
)
FRONT_MATTER_RE = re.compile(r"\A\ufeff?---\s*\r?\n.*?\r?\n---\s*(?:\r?\n|\Z)", re.DOTALL)
REFERENCE_DEFINITION_RE = re.compile(r"^\s*\[(?!\^)[^\]]+\]:\s*(<[^>]+>|\S+)", re.MULTILINE)
EVIDENCE_ROW_RE = re.compile(r"^\|\s*(?:code|doc)\s*\|\s*(.*?)\s*\|", re.MULTILINE)
INITIALIZATION_PLACEHOLDER_RE = re.compile(r"\{\{初始化:[^{}\r\n]+\}\}")
FULL_MARKDOWN_LINK_RE = re.compile(r"^\[[^\]\r\n]+\]\((.+)\)$")
FENCE_LINE_RE = re.compile(r"^ {0,3}(?P<run>`{3,}|~{3,})(?P<rest>[^\r\n]*)(?:\r?\n)?$")
ARCHIVE_MIRROR_ROOTS = {
    "main",
    "applications",
    "candidate",
    "personal",
    "reference",
    "template",
}
SCATTERED_ARCHIVE_NAMES = {
    "archive",
    "archived",
    "deprecated",
    "legacy",
    "obsolete",
    "历史",
    "归档",
}
RAW_REFERENCE_MARKER = ".raw-reference"
AGENTS_ROUTING_HEADING = "文档与知识路由"
AGENTS_REQUIRED_HEADINGS = (
    "项目概述",
    "技术栈",
    "目录与模块职责",
    "运行与开发方式",
    "验证策略",
    "项目特有规则",
)
AGENTS_ROUTING_TARGETS = (
    "knowledge/README.md",
    "knowledge/ROUTING.md",
    "docs/changes/README.md",
    "docs/postmortem/README.md",
)
ROUTING_REQUIRED_TARGETS = (
    "docs/changes/",
    "docs/postmortem/",
    "knowledge/reference/",
    "knowledge/personal/",
    "knowledge/archive/",
    "knowledge/template/",
    "knowledge/candidate/",
    "knowledge/main/",
    "knowledge/applications/",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", nargs="?", help="工作区根目录；默认从脚本位置定位")
    git_group = parser.add_mutually_exclusive_group()
    git_group.add_argument(
        "--git-staged",
        action="store_true",
        help="校验暂存区中的知识归档移动是否保持原相对路径",
    )
    git_group.add_argument(
        "--git-range",
        metavar="BASE..HEAD",
        help="校验指定 Git 提交范围中的知识归档移动，供 CI 或推送前流程使用",
    )
    return parser.parse_args()


def is_template(path: Path) -> bool:
    parts = tuple(part.lower() for part in path.parts)
    return (
        parts[:2] == ("knowledge", "template")
        or parts[:3] == ("knowledge", "archive", "template")
        or parts[:3] == ("docs", "changes", "templates")
        or parts[:3] == ("docs", "postmortem", "templates")
    )


def is_raw_reference(workspace: Path, relative: Path) -> bool:
    """通过显式标记识别原始导入资料，避免绑定具体项目或资料名称。"""
    path = workspace / relative
    for root_relative in (
        Path("knowledge/reference"),
        Path("knowledge/archive/reference"),
    ):
        root = workspace / root_relative
        if not is_within_workspace(path, root):
            continue
        current = path if path.is_dir() else path.parent
        while current != root and is_within_workspace(current, root):
            if (current / RAW_REFERENCE_MARKER).is_file():
                return True
            current = current.parent
    return False


def fence_line(line: str) -> tuple[str, str] | None:
    match = FENCE_LINE_RE.match(line)
    if match is None:
        return None
    return match.group("run"), match.group("rest")


def is_closing_fence(token: tuple[str, str], opening: str) -> bool:
    run, rest = token
    return run[0] == opening[0] and len(run) >= len(opening) and not rest.strip()


def is_opening_fence(token: tuple[str, str]) -> bool:
    run, rest = token
    return not (run[0] == "`" and "`" in rest)


def markdown_fenced_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    opening: str | None = None
    info = ""
    body: list[str] = []
    for line in text.splitlines(keepends=True):
        token = fence_line(line)
        if opening is None:
            if token is not None and is_opening_fence(token):
                opening, info = token
                body = []
            continue
        if token is not None and is_closing_fence(token, opening):
            blocks.append((info.strip(), "".join(body)))
            opening = None
            info = ""
            body = []
            continue
        body.append(line)
    return blocks


def without_code_fences(text: str, *, strip_inline: bool = True) -> str:
    lines: list[str] = []
    opening: str | None = None
    for line in text.splitlines(keepends=True):
        token = fence_line(line)
        if opening is None and token is not None and is_opening_fence(token):
            opening = token[0]
            continue
        if opening is not None and token is not None and is_closing_fence(token, opening):
            opening = None
            continue
        if opening is None:
            lines.append(line)
    result = "".join(lines)
    return re.sub(r"`[^`\r\n]*`", "", result) if strip_inline else result


def managed_markdown(workspace: Path) -> list[Path]:
    paths: list[Path] = []
    agents = workspace / "AGENTS.md"
    if agents.is_file():
        paths.append(agents)
    for root_name in ("knowledge", "docs"):
        root = workspace / root_name
        if root.exists():
            paths.extend(path for path in root.rglob("*.md") if path.is_file())
    return sorted(paths)


def without_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def mask_fenced_blocks(text: str) -> str:
    """遮蔽代码围栏并保留字符位置，避免示例标题参与章节识别。"""
    result = list(text)
    opening: str | None = None
    offset = 0
    for line in text.splitlines(keepends=True):
        token = fence_line(line)
        was_inside = opening is not None
        if not was_inside and token is not None and is_opening_fence(token):
            opening = token[0]
        if was_inside or opening is not None:
            for index, char in enumerate(line, start=offset):
                if char not in "\r\n":
                    result[index] = " "
        if was_inside and token is not None and is_closing_fence(token, opening):
            opening = None
        offset += len(line)
    return "".join(result)


def markdown_section(
    text: str,
    heading: str,
    levels: tuple[int, ...],
    *,
    source_text: str | None = None,
) -> str | None:
    marks_pattern = "|".join("#" * level for level in levels)
    match = re.search(
        rf"^(?P<marks>{marks_pattern})[ \t]+{re.escape(heading)}[ \t]*$",
        text,
        re.MULTILINE,
    )
    if match is None:
        return None
    level = len(match.group("marks"))
    end = re.search(rf"^#{{1,{level}}}\s+", text[match.end() :], re.MULTILINE)
    end_index = match.end() + end.start() if end else len(text)
    source = source_text if source_text is not None else text
    return source[match.end() : end_index]


def meaningful_section_body(section: str) -> str:
    text = without_html_comments(section)
    text = re.sub(r"^\s*(?:```|~~~).*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*#{1,6}\s+.*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*(?:---+|___+|\*\*\*+)\s*$", "", text, flags=re.MULTILINE)
    return text.strip()


def normalized_workspace_target(workspace: Path, raw_target: str) -> str | None:
    target = local_target(raw_target)
    if target is None:
        return None
    target_path = Path(target)
    if target_path.is_absolute():
        return None
    resolved = (workspace / target_path).resolve()
    if not is_within_workspace(resolved, workspace):
        return None
    return resolved.relative_to(workspace).as_posix()


def detailed_routing_signal_count(text: str) -> int:
    patterns = (
        r"\[(?:proposed|implemented|rejected|archived)/\]",
        r"knowledge/candidate/(?:main|applications|unclassified)/",
        r"knowledge/applications/[<{]?appCode[>}]?/",
        r"\[(?:base|feature|rule|tech)/\]",
    )
    return sum(len(set(re.findall(pattern, text))) for pattern in patterns)


def validate_agents_routing(workspace: Path, errors: list[str]) -> None:
    targets = (
        workspace / "AGENTS.md",
        workspace / "knowledge" / "template" / "common" / "AGENTS-template.md",
    )
    for path in targets:
        if not path.is_file():
            relative = path.relative_to(workspace).as_posix()
            errors.append(f"AGENTS 结构：{relative} 必须是普通文件")
            continue
        relative = path.relative_to(workspace).as_posix()
        raw_text = path.read_text(encoding="utf-8-sig")
        text = without_html_comments(raw_text)
        heading_text = mask_fenced_blocks(text)
        for heading in AGENTS_REQUIRED_HEADINGS:
            count = len(
                re.findall(
                    rf"^##[ \t]+{re.escape(heading)}[ \t]*$",
                    heading_text,
                    re.MULTILINE,
                )
            )
            if count != 1:
                errors.append(
                    f"AGENTS 结构：{relative} 必须且只能包含一个“## {heading}”章节"
                )
                continue
            section = markdown_section(
                heading_text, heading, (2,), source_text=text
            )
            if section is None or not meaningful_section_body(section):
                errors.append(f"AGENTS 结构：{relative} 的“## {heading}”章节不能为空")

        route_headings = re.findall(
            rf"^###?[ \t]+{re.escape(AGENTS_ROUTING_HEADING)}[ \t]*$",
            heading_text,
            re.MULTILINE,
        )
        route_section = markdown_section(
            heading_text,
            AGENTS_ROUTING_HEADING,
            (2, 3),
            source_text=text,
        )
        if len(route_headings) != 1 or route_section is None:
            errors.append(
                f"AGENTS 路由：{relative} 必须且只能包含一个"
                f"“{AGENTS_ROUTING_HEADING}”章节"
            )
        else:
            route_text = without_html_comments(without_code_fences(route_section))
            targets_found = [
                normalized
                for raw_target in inline_link_targets(route_text)
                if (normalized := normalized_workspace_target(workspace, raw_target))
                is not None
            ]
            for target in AGENTS_ROUTING_TARGETS:
                if targets_found.count(target) != 1:
                    errors.append(
                        f"AGENTS 路由：{relative} 的路由章节必须且只能链接一次 {target}"
                    )
        if re.search(r"^#{2,6}[ \t]+总路由图[ \t]*$", heading_text, re.MULTILINE):
            errors.append(
                f"AGENTS 路由：{relative} 不得复制 knowledge/ROUTING.md 的总路由图"
            )
        if detailed_routing_signal_count(raw_text) >= 6:
            errors.append(
                f"AGENTS 路由：{relative} 包含完整路由的详细分类，应只保留精简入口"
            )

    routing = workspace / "knowledge" / "ROUTING.md"
    if not routing.is_file():
        errors.append("AGENTS 路由：knowledge/ROUTING.md 必须是普通文件")
    else:
        routing_text = without_html_comments(routing.read_text(encoding="utf-8-sig"))
        routing_heading_text = mask_fenced_blocks(routing_text)
        routing_headings = re.findall(
            r"^##[ \t]+总路由图[ \t]*$", routing_heading_text, re.MULTILINE
        )
        total_section = markdown_section(
            routing_heading_text, "总路由图", (2,), source_text=routing_text
        )
        if len(routing_headings) != 1 or total_section is None:
            errors.append(
                "AGENTS 路由：knowledge/ROUTING.md 必须且只能包含一个“## 总路由图”章节"
            )
        else:
            fenced_blocks = markdown_fenced_blocks(total_section)
            route_graph = "\n".join(
                body
                for info, body in fenced_blocks
                if info.lower() == "text" and body.strip()
            )
            if not route_graph:
                errors.append(
                    "AGENTS 路由：knowledge/ROUTING.md 的“总路由图”必须包含非空文本图"
                )
            else:
                normalized_graph = route_graph.replace("[", "").replace("]", "")
                for target in ROUTING_REQUIRED_TARGETS:
                    if target not in normalized_graph:
                        errors.append(
                            "AGENTS 路由：knowledge/ROUTING.md 的“总路由图”"
                            f"缺少顶层去向 {target}"
                        )


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
        if is_raw_reference(workspace, relative):
            continue
        if FRONT_MATTER_RE.match(path.read_text(encoding="utf-8-sig")):
            errors.append(f"YAML 头：{relative.as_posix()} 不应包含自定义 Front Matter")


def validate_links(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_raw_reference(workspace, relative):
            continue
        template_path = is_template(relative)
        template_root_index = relative == Path("knowledge/template/INDEX.md")
        if (
            template_path
            and relative.parts[:2] == ("knowledge", "template")
            and not template_root_index
        ):
            continue
        text = without_html_comments(
            without_code_fences(path.read_text(encoding="utf-8-sig"))
        )
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
        if is_template(relative) or is_raw_reference(workspace, relative):
            continue
        text = without_html_comments(
            without_code_fences(
                path.read_text(encoding="utf-8-sig"), strip_inline=False
            )
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
    text = without_html_comments(
        without_code_fences(index_path.read_text(encoding="utf-8-sig"))
    )
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
        checked_template_root_indexes = {
            Path("knowledge/template/INDEX.md"),
            Path("knowledge/archive/template/INDEX.md"),
        }
        if (
            is_template(relative) and relative not in checked_template_root_indexes
        ) or is_raw_reference(workspace, relative):
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


def validate_application_identity(
    workspace: Path, app_codes: set[str], errors: list[str]
) -> None:
    for code in sorted(app_codes):
        root = workspace / "knowledge" / "applications" / code
        overview = root / f"{code}.md"
        readme = root / "README.md"
        index = root / "INDEX.md"
        if not overview.is_file() or not readme.is_file() or not index.is_file():
            continue  # 缺失文件由目录骨架校验统一报告。

        overview_text = without_html_comments(
            without_code_fences(
                overview.read_text(encoding="utf-8-sig"), strip_inline=False
            )
        )
        values = APP_CODE_ROW_RE.findall(overview_text)
        if values != [code]:
            display = ", ".join(values) if values else "未找到"
            errors.append(
                f"应用身份：knowledge/applications/{code}/{code}.md 的“应用编码”"
                f"必须且只能是 {code}，当前为 {display}"
            )

        readme_text = without_html_comments(
            without_code_fences(
                readme.read_text(encoding="utf-8-sig"), strip_inline=False
            )
        )
        expected_boundary = f"applications/{code}/"
        if expected_boundary not in readme_text:
            errors.append(
                f"应用身份：knowledge/applications/{code}/README.md "
                f"必须声明 {expected_boundary}"
            )

        overview_target = overview.resolve()
        if overview_target not in index_targets(index):
            errors.append(
                f"应用身份：knowledge/applications/{code}/INDEX.md "
                f"必须链接 {code}.md"
            )


def validate_archive_layout(workspace: Path, errors: list[str]) -> None:
    knowledge = workspace / "knowledge"
    archive = knowledge / "archive"
    if not archive.is_dir():
        errors.append("归档结构：缺少 knowledge/archive")
        return

    direct_directories = {path.name for path in archive.iterdir() if path.is_dir()}
    missing = sorted(ARCHIVE_MIRROR_ROOTS - direct_directories)
    unexpected = sorted(direct_directories - ARCHIVE_MIRROR_ROOTS)
    if missing:
        errors.append(f"归档结构：缺少镜像目录：{', '.join(missing)}")
    if unexpected:
        errors.append(f"归档结构：存在非镜像根目录：{', '.join(unexpected)}")

    unexpected_root_files = sorted(
        path.name
        for path in archive.iterdir()
        if path.is_file() and path.name not in {"README.md", "INDEX.md"}
    )
    if unexpected_root_files:
        errors.append(
            "归档结构：归档内容不能直接放在 archive 根目录："
            + ", ".join(unexpected_root_files)
        )

    for name in sorted(ARCHIVE_MIRROR_ROOTS):
        root = archive / name
        for infrastructure in ("README.md", "INDEX.md"):
            if root.is_dir() and not (root / infrastructure).is_file():
                errors.append(f"归档结构：缺少 archive/{name}/{infrastructure}")

    archive_resolved = archive.resolve()
    for path in knowledge.rglob("*"):
        is_junction = getattr(path, "is_junction", lambda: False)()
        if path.is_symlink() or is_junction:
            errors.append(
                "归档结构：knowledge/ 不允许文件或目录符号链接或 junction："
                f"{path.relative_to(workspace).as_posix()}"
            )
            continue
        if not path.is_dir():
            continue
        resolved = path.resolve()
        if path == archive or archive in path.parents:
            continue
        if resolved == archive_resolved or archive_resolved in resolved.parents:
            errors.append(
                "归档结构：发现指向 knowledge/archive 的旁路目录链接："
                f"{path.relative_to(workspace).as_posix()}"
            )
            continue
        if is_raw_reference(workspace, path.relative_to(workspace)):
            continue
        if path.name.lower() in SCATTERED_ARCHIVE_NAMES:
            errors.append(
                "归档结构：发现旁路归档目录，内容必须移动到 knowledge/archive："
                f"{path.relative_to(workspace).as_posix()}"
            )

    reference_roots = (
        knowledge / "reference",
        archive / "reference",
    )
    for marker in knowledge.rglob(RAW_REFERENCE_MARKER):
        parent = marker.parent
        allowed = any(
            parent != root and is_within_workspace(parent, root)
            for root in reference_roots
        )
        if not allowed:
            errors.append(
                "原始资料标记：.raw-reference 只能放在 reference 的资料子目录根部："
                f"{marker.relative_to(workspace).as_posix()}"
            )
        if marker.is_symlink() or not marker.is_file():
            errors.append(
                "原始资料标记：.raw-reference 必须是普通文件："
                f"{marker.relative_to(workspace).as_posix()}"
            )


def archive_mapping(path: str) -> str | None:
    parts = Path(path).parts
    if (
        len(parts) < 3
        or parts[0] != "knowledge"
        or parts[1] not in ARCHIVE_MIRROR_ROOTS
    ):
        return None
    if len(parts) == 3 and parts[2] in {"README.md", "INDEX.md"}:
        return None
    return Path("knowledge", "archive", parts[1], *parts[2:]).as_posix()


def active_mapping(path: str) -> str | None:
    parts = Path(path).parts
    if (
        len(parts) < 4
        or parts[:2] != ("knowledge", "archive")
        or parts[2] not in ARCHIVE_MIRROR_ROOTS
    ):
        return None
    if len(parts) == 4 and parts[3] in {"README.md", "INDEX.md"}:
        return None
    return Path("knowledge", parts[2], *parts[3:]).as_posix()


def git_name_status(
    workspace: Path, *, staged: bool, revision_range: str | None
) -> list[tuple[str, str, str | None]]:
    if revision_range and (
        revision_range.startswith("-")
        or any(char.isspace() for char in revision_range)
    ):
        raise ValueError("Git 提交范围不能以 '-' 开头或包含空白字符")
    command = [
        "git",
        "diff",
        "--name-status",
        "-z",
        "--find-renames",
        "--find-copies-harder",
    ]
    if staged:
        unstaged = subprocess.run(
            ["git", "diff", "--name-only", "-z", "--", "knowledge"],
            cwd=workspace,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if unstaged.returncode:
            message = unstaged.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(message or "无法检查 knowledge/ 未暂存改动")
        unstaged_paths = [
            path
            for path in unstaged.stdout.decode(
                "utf-8", errors="surrogateescape"
            ).split("\0")
            if path
        ]
        if unstaged_paths:
            preview = ", ".join(unstaged_paths[:5])
            suffix = "..." if len(unstaged_paths) > 5 else ""
            raise RuntimeError(
                "--git-staged 要求 knowledge/ 没有未暂存改动："
                f"{preview}{suffix}"
            )
        untracked = subprocess.run(
            [
                "git",
                "ls-files",
                "--others",
                "--exclude-standard",
                "-z",
                "--",
                "knowledge",
            ],
            cwd=workspace,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if untracked.returncode:
            message = untracked.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(message or "无法检查 knowledge/ 未跟踪文件")
        untracked_paths = [
            path
            for path in untracked.stdout.decode(
                "utf-8", errors="surrogateescape"
            ).split("\0")
            if path
        ]
        if untracked_paths:
            preview = ", ".join(untracked_paths[:5])
            suffix = "..." if len(untracked_paths) > 5 else ""
            raise RuntimeError(
                "--git-staged 要求 knowledge/ 没有未跟踪文件："
                f"{preview}{suffix}"
            )
        command.append("--cached")
    elif revision_range:
        command.append(revision_range)
    command.extend(("--", "knowledge"))
    completed = subprocess.run(
        command,
        cwd=workspace,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(message or "git diff 执行失败")
    fields = completed.stdout.decode("utf-8", errors="surrogateescape").split("\0")
    changes: list[tuple[str, str, str | None]] = []
    index = 0
    while index < len(fields) and fields[index]:
        status = fields[index]
        index += 1
        if status.startswith(("R", "C")):
            if index + 1 >= len(fields):
                raise RuntimeError("无法解析 git diff 的重命名记录")
            old_path, new_path = fields[index], fields[index + 1]
            index += 2
            changes.append((status, old_path, new_path))
        else:
            if index >= len(fields):
                raise RuntimeError("无法解析 git diff 的文件记录")
            changes.append((status, fields[index], None))
            index += 1
    return changes


def validate_git_archive_moves(
    workspace: Path,
    errors: list[str],
    *,
    staged: bool,
    revision_range: str | None,
) -> None:
    try:
        changes = git_name_status(
            workspace, staged=staged, revision_range=revision_range
        )
    except (OSError, RuntimeError, ValueError) as exc:
        errors.append(f"Git 归档映射：{exc}")
        return

    deleted = {
        old_path
        for status, old_path, new_path in changes
        if status.startswith("D") and new_path is None
    }
    for status, old_path, new_path in changes:
        destination = new_path if new_path is not None else old_path
        expected_source = active_mapping(destination)
        old_is_archive = new_path is not None and active_mapping(old_path) is not None
        if expected_source is not None and not old_is_archive:
            if status.startswith("R"):
                if old_path != expected_source:
                    errors.append(
                        "Git 归档映射：归档目标未保留来源相对路径："
                        f"{old_path} -> {destination}，应来自 {expected_source}"
                    )
            elif status.startswith("C"):
                errors.append(
                    "Git 归档映射：归档必须移动而非复制："
                    f"{old_path} -> {destination}"
                )
            elif status.startswith("A"):
                if expected_source in deleted:
                    errors.append(
                        "Git 归档映射：归档必须是 Git 可识别的移动，不能以独立新增和删除代替："
                        f"{expected_source} -> {destination}"
                    )
                else:
                    errors.append(
                        "Git 归档映射：新增归档文件缺少对应来源移动："
                        f"{destination}，应移动自 {expected_source}"
                    )

        expected_archive = archive_mapping(destination)
        if expected_archive is not None:
            if status.startswith("A") and expected_archive in deleted:
                errors.append(
                    "Git 归档映射：恢复必须是 Git 可识别的移动，不能以独立新增和删除代替："
                    f"{expected_archive} -> {destination}"
                )
            elif new_path is not None and status.startswith("C") and active_mapping(old_path):
                errors.append(
                    "Git 归档映射：恢复有效知识必须移动而非复制："
                    f"{old_path} -> {destination}"
                )
            elif (
                new_path is not None
                and status.startswith("R")
                and active_mapping(old_path)
                and old_path != expected_archive
            ):
                errors.append(
                    "Git 归档映射：恢复路径未遵循归档反向映射："
                    f"{old_path} -> {destination}，应来自 {expected_archive}"
                )


def validate_required_layout(workspace: Path, app_codes: set[str], errors: list[str]) -> None:
    required = [
        "AGENTS.md",
        "knowledge/README.md",
        "knowledge/INDEX.md",
        "knowledge/ROUTING.md",
        "knowledge/main/README.md",
        "knowledge/main/INDEX.md",
        "knowledge/applications/README.md",
        "knowledge/applications/INDEX.md",
        "knowledge/candidate/README.md",
        "knowledge/candidate/INDEX.md",
        "knowledge/candidate/applications/README.md",
        "knowledge/candidate/applications/INDEX.md",
        "knowledge/candidate/main/README.md",
        "knowledge/candidate/main/INDEX.md",
        "knowledge/personal/README.md",
        "knowledge/personal/INDEX.md",
        "knowledge/archive/README.md",
        "knowledge/archive/INDEX.md",
        "knowledge/archive/main/README.md",
        "knowledge/archive/main/INDEX.md",
        "knowledge/archive/applications/README.md",
        "knowledge/archive/applications/INDEX.md",
        "knowledge/archive/candidate/README.md",
        "knowledge/archive/candidate/INDEX.md",
        "knowledge/archive/personal/README.md",
        "knowledge/archive/personal/INDEX.md",
        "knowledge/archive/reference/README.md",
        "knowledge/archive/reference/INDEX.md",
        "knowledge/archive/template/README.md",
        "knowledge/archive/template/INDEX.md",
        "knowledge/reference/README.md",
        "knowledge/reference/INDEX.md",
        "knowledge/scripts/.gitignore",
        "knowledge/scripts/README.md",
        "knowledge/scripts/validate.py",
        "knowledge/scripts/validate_candidate.py",
        "knowledge/scripts/validate_docs.py",
        "knowledge/scripts/validate_personal.py",
        "knowledge/scripts/validate_skills.py",
        "knowledge/template/README.md",
        "knowledge/template/INDEX.md",
        "knowledge/template/common/README-template.md",
        "knowledge/template/common/INDEX-template.md",
        "knowledge/template/common/AGENTS-template.md",
        "knowledge/template/candidate/README.md",
        "knowledge/template/candidate/candidate.md",
        "knowledge/template/personal/README.md",
        "knowledge/template/personal/{ownerCode}/README.md",
        "knowledge/template/personal/{ownerCode}/INDEX.md",
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
        if not (workspace / relative).is_file():
            errors.append(f"目录骨架：缺少普通文件 {relative}")


def validate_placeholders(workspace: Path, paths: list[Path], errors: list[str]) -> None:
    for path in paths:
        relative = path.relative_to(workspace)
        if is_template(relative) or is_raw_reference(workspace, relative):
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
    args = parse_args()
    default_workspace = Path(__file__).resolve().parents[2]
    workspace = Path(args.workspace).resolve() if args.workspace else default_workspace
    errors: list[str] = []
    paths = managed_markdown(workspace)
    validate_agents_routing(workspace, errors)
    validate_no_frontmatter(workspace, paths, errors)
    validate_links(workspace, paths, errors)
    validate_evidence_rows(workspace, paths, errors)
    validate_indexes(workspace, errors)
    app_codes = application_codes(workspace, errors)
    validate_application_identity(workspace, app_codes, errors)
    validate_candidate_layout(workspace, errors)
    validate_personal_layout(workspace, errors)
    validate_docs_layout(workspace, errors)
    validate_project_skills(workspace, errors)
    validate_archive_layout(workspace, errors)
    if args.git_staged or args.git_range:
        validate_git_archive_moves(
            workspace,
            errors,
            staged=args.git_staged,
            revision_range=args.git_range,
        )
    validate_required_layout(workspace, app_codes, errors)
    validate_placeholders(workspace, paths, errors)

    if errors:
        print(f"知识与研发文档校验失败，共 {len(errors)} 个错误：")
        for error in errors:
            print(f"- {error}")
        return 1

    raw_count = sum(
        is_raw_reference(workspace, path.relative_to(workspace)) for path in paths
    )
    managed_count = len(paths) - raw_count
    git_summary = (
        "；Git 归档移动映射已检查"
        if args.git_staged or args.git_range
        else ""
    )
    print(
        "知识与研发文档校验通过："
        f"已检查 {managed_count} 个受管理 Markdown 文件，跳过 {raw_count} 个原始导入参考文件；"
        "AGENTS 必选结构与路由、YAML 头、目录骨架、相对链接、正文证据、应用身份、候选契约、个人所有者边界、Change/Postmortem 实例、标准目录中的项目 Skill、归档镜像、索引和占位符均已检查"
        f"{git_summary}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
