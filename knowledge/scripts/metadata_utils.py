#!/usr/bin/env python3
"""Shared helpers for Knowledge metadata scripts (validate_metadata / metadata_report).

This module is imported by both scripts. It contains:
- repository root / knowledge dir location
- Registry loading from KNOWLEDGE-METADATA-RULES.md
- Markdown scanning (excluding reference/template/scripts)
- Front Matter parsing (UTF-8 BOM compatible)

It performs NO validation and NO mutation of any file.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Constants: system-closed enums (must not be hardcoded as registries).
# ---------------------------------------------------------------------------

SCOPE_VALUES = {"global", "app", "cross-app"}
STATUS_VALUES = {"DRAFT", "CANDIDATE", "OFFICIAL", "DEPRECATED"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
STABILITY_VALUES = {"stable", "evolving", "volatile"}
EVIDENCE_TYPE_VALUES = {"code", "doc", "human"}

# Allowed front matter fields. Anything else -> WARNING (validator-specific).
ALLOWED_FIELDS = {
    "id",
    "type",
    "scope",
    "appCode",
    "status",
    "owner",
    "maintainers",
    "version",
    "updatedAt",
    "verifiedAt",
    "confidence",
    "stability",
    "evidence",
    "tags",
    "anchors",
}

ID_RE = re.compile(r"^KB-[A-Z0-9]+(?:-[A-Z0-9]+)+$")
TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ANCHOR_RE = re.compile(r"^([A-Z][A-Z0-9-]*):([A-Z0-9]+(?:-[A-Z0-9]+)*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Directories excluded from scanning.
EXCLUDE_DIRS = {"reference", "template", "scripts"}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class Registry:
    """Dynamic project registries read from KNOWLEDGE-METADATA-RULES.md."""

    app_codes: set[str] = field(default_factory=set)
    custom_types: set[str] = field(default_factory=set)
    owners: set[str] = field(default_factory=set)
    users: set[str] = field(default_factory=set)
    custom_anchor_namespaces: set[str] = field(default_factory=set)
    built_in_types: set[str] = field(default_factory=set)
    built_in_anchor_namespaces: set[str] = field(default_factory=set)

    @property
    def valid_types(self) -> set[str]:
        return self.built_in_types | self.custom_types

    @property
    def valid_anchor_namespaces(self) -> set[str]:
        return self.built_in_anchor_namespaces | self.custom_anchor_namespaces


@dataclass
class FileIssue:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def has_error(self) -> bool:
        return len(self.errors) > 0


# ---------------------------------------------------------------------------
# Locating repository root & knowledge dir
# ---------------------------------------------------------------------------


def find_repo_root(start: str) -> str:
    """Walk upward from ``start`` until a ``.git`` directory is found."""
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            # Fallback: assume the script's grandparent is the repo root.
            return os.path.abspath(os.path.join(start, "..", ".."))
        cur = parent


def find_knowledge_dir(repo_root: str) -> str:
    return os.path.join(repo_root, "knowledge")


def find_rules_path(knowledge_dir: str) -> str:
    return os.path.join(knowledge_dir, "KNOWLEDGE-METADATA-RULES.md")


# ---------------------------------------------------------------------------
# Reading registries from the rules file
# ---------------------------------------------------------------------------


def _extract_block(text: str, begin_marker: str, end_marker: str) -> str | None:
    """Return the text between BEGIN/END comment markers (inclusive of markers)."""
    begin = text.find(begin_marker)
    if begin == -1:
        return None
    end = text.find(end_marker, begin)
    if end == -1:
        return None
    end += len(end_marker)
    return text[begin:end]


def _parse_yaml_block(block: str | None) -> dict[str, Any]:
    if block is None:
        return {}
    # Strip comment markers and any ```yaml ... ``` fences, keep only YAML.
    lines = block.splitlines()
    yaml_lines = []
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("<!--") and stripped.endswith("-->"):
            continue
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        yaml_lines.append(line)
    try:
        data = yaml.safe_load("\n".join(yaml_lines))
    except yaml.YAMLError:
        return {}
    if not isinstance(data, dict):
        return {}
    return data


def load_registries(rules_path: str) -> Registry:
    """Read project registries and built-in values from the rules file."""
    with open(rules_path, encoding="utf-8-sig") as f:
        text = f.read()

    reg = Registry()

    # App codes
    block = _extract_block(
        text, "<!-- KB-REGISTRY:APP-CODE:BEGIN -->", "<!-- KB-REGISTRY:APP-CODE:END -->"
    )
    data = _parse_yaml_block(block)
    reg.app_codes = set(data.get("appCodes", []) or [])

    # Custom types
    block = _extract_block(
        text,
        "<!-- KB-REGISTRY:CUSTOM-TYPE:BEGIN -->",
        "<!-- KB-REGISTRY:CUSTOM-TYPE:END -->",
    )
    data = _parse_yaml_block(block)
    reg.custom_types = set(data.get("customTypes", []) or [])

    # Owners
    block = _extract_block(
        text, "<!-- KB-REGISTRY:OWNER:BEGIN -->", "<!-- KB-REGISTRY:OWNER:END -->"
    )
    data = _parse_yaml_block(block)
    reg.owners = set(data.get("owners", []) or [])

    # Users
    block = _extract_block(
        text, "<!-- KB-REGISTRY:USER:BEGIN -->", "<!-- KB-REGISTRY:USER:END -->"
    )
    data = _parse_yaml_block(block)
    reg.users = set(data.get("users", []) or [])

    # Custom anchor namespaces
    block = _extract_block(
        text,
        "<!-- KB-REGISTRY:ANCHOR-NAMESPACE:BEGIN -->",
        "<!-- KB-REGISTRY:ANCHOR-NAMESPACE:END -->",
    )
    data = _parse_yaml_block(block)
    reg.custom_anchor_namespaces = set(data.get("customAnchorNamespaces", []) or [])

    # Built-in types (static in rules, not behind a registry marker)
    m = re.search(r"builtInTypes:\s*\n((?:[ \t]*-[ \t]*[^\n]+\n?)+)", text)
    if m:
        reg.built_in_types = set(
            item.strip()[1:].strip()
            for item in m.group(1).splitlines()
            if item.strip().startswith("-")
        )

    # Built-in anchor namespaces (static in rules)
    m = re.search(r"builtInAnchorNamespaces:\s*\n((?:[ \t]*-[ \t]*[^\n]+\n?)+)", text)
    if m:
        reg.built_in_anchor_namespaces = set(
            item.strip()[1:].strip()
            for item in m.group(1).splitlines()
            if item.strip().startswith("-")
        )

    return reg


# ---------------------------------------------------------------------------
# Scanning markdown files
# ---------------------------------------------------------------------------


def find_markdown_files(knowledge_dir: str) -> list[str]:
    """Recursively find *.md files under knowledge_dir, excluding reference/, template/, scripts/."""
    results: list[str] = []
    for root, dirs, files in os.walk(knowledge_dir):
        # Prune excluded directories in-place.
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for name in files:
            if name.lower().endswith(".md"):
                results.append(os.path.join(root, name))
    return sorted(results)


# ---------------------------------------------------------------------------
# Front matter parsing
# ---------------------------------------------------------------------------


def parse_front_matter(path: str) -> tuple[dict[str, Any] | None, str | None]:
    """Return (front_matter_dict, error_message).

    front_matter_dict is None when there is no front matter.
    error_message is set when YAML fails to parse.
    """
    with open(path, encoding="utf-8-sig") as f:
        content = f.read()

    if not content.startswith("---"):
        return None, None

    # Find the closing '---' delimiter.
    lines = content.splitlines()
    # lines[0] is the opening '---'
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        return None, "missing closing '---' for front matter"

    fm_text = "\n".join(lines[1:end_idx])
    try:
        data = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"

    if data is None:
        data = {}
    if not isinstance(data, dict):
        return None, "front matter is not a YAML mapping"
    return data, None


# ---------------------------------------------------------------------------
# Date helper
# ---------------------------------------------------------------------------


def parse_date(value: Any) -> date | None:
    """Return a ``datetime.date`` if value is a real YYYY-MM-DD date, else None.

    Accepts both ``str`` and ``datetime.date`` (PyYAML parses unquoted dates
    into date objects).
    """
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def is_knowledge_file(fm: dict[str, Any]) -> bool:
    """A file with a ``type`` field is a Knowledge content file."""
    return "type" in fm
