#!/usr/bin/env python3
"""Knowledge Front Matter metadata validation script (read-only).

Validates Knowledge Markdown files against the rules defined in
``knowledge/KNOWLEDGE-METADATA-RULES.md``. This script NEVER modifies any file.

Usage:
    python knowledge/scripts/validate_metadata.py [--verbose]

Exit codes:
    0  -> no ERROR found (WARNINGs allowed)
    1  -> at least one ERROR found
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

import yaml

from metadata_utils import (
    ALLOWED_FIELDS,
    ANCHOR_RE,
    CONFIDENCE_VALUES,
    DATE_RE,
    EVIDENCE_TYPE_VALUES,
    ID_RE,
    SCOPE_VALUES,
    STABILITY_VALUES,
    STATUS_VALUES,
    TAG_RE,
    Registry,
    FileIssue,
    find_knowledge_dir,
    find_markdown_files,
    find_repo_root,
    is_knowledge_file,
    load_registries,
    parse_date,
    parse_front_matter,
)

# ---------------------------------------------------------------------------
# Validation helpers (validator-specific)
# ---------------------------------------------------------------------------


def _is_real_int(value: Any) -> bool:
    """True only for int that is not bool."""
    return isinstance(value, int) and not isinstance(value, bool)


# ---------------------------------------------------------------------------
# Global field validation
# ---------------------------------------------------------------------------


REQUIRED_GLOBAL_FIELDS = [
    "id",
    "scope",
    "status",
    "owner",
    "maintainers",
    "version",
    "updatedAt",
    "verifiedAt",
    "tags",
    "anchors",
]


def validate_global_fields(
    fm: dict[str, Any], reg: Registry, issues: FileIssue
) -> None:
    # 7. required fields
    for field_name in REQUIRED_GLOBAL_FIELDS:
        if field_name not in fm:
            issues.errors.append(f"missing required field: {field_name}")

    # 8.1 id
    fm_id = fm.get("id")
    if fm_id is not None:
        if not isinstance(fm_id, str) or not ID_RE.match(fm_id):
            issues.errors.append(f"invalid id format: {fm_id!r} (expected KB-CATEGORY-KEY)")

    # 8.2 scope
    scope = fm.get("scope")
    if scope is not None:
        if scope not in SCOPE_VALUES:
            issues.errors.append(f"invalid scope: {scope!r} (expected one of {sorted(SCOPE_VALUES)})")

    # 8.3 appCode
    app_code = fm.get("appCode")
    if scope == "app":
        if app_code is None:
            issues.errors.append("missing appCode (required when scope=app)")
        elif not isinstance(app_code, str) or app_code not in reg.app_codes:
            issues.errors.append(f"invalid appCode: {app_code!r} (not registered)")
    elif scope in ("global", "cross-app"):
        if app_code is not None:
            issues.errors.append("unexpected appCode (forbidden when scope=%s)" % scope)
    elif app_code is not None:
        # scope invalid already reported; still flag unexpected field presence.
        if not isinstance(app_code, str) or app_code not in reg.app_codes:
            issues.errors.append(f"invalid appCode: {app_code!r} (not registered)")

    # 8.4 status
    status = fm.get("status")
    if status is not None and status not in STATUS_VALUES:
        issues.errors.append(f"invalid status: {status!r} (expected one of {sorted(STATUS_VALUES)})")

    # 8.5 owner
    owner = fm.get("owner")
    if owner is not None:
        if not isinstance(owner, str) or not owner.strip() or owner not in reg.owners:
            issues.errors.append(f"invalid owner: {owner!r} (not registered or empty)")

    # 8.6 maintainers
    maintainers = fm.get("maintainers")
    if maintainers is not None:
        if not isinstance(maintainers, list) or len(maintainers) == 0:
            issues.errors.append("invalid maintainers (must be a non-empty list)")
        else:
            for m in maintainers:
                if not isinstance(m, str) or not m.strip() or m not in reg.users:
                    issues.errors.append(f"invalid maintainer: {m!r} (not registered or empty)")

    # 8.7 version
    version = fm.get("version")
    if version is not None:
        if not _is_real_int(version) or version < 1:
            issues.errors.append(f"invalid version: {version!r} (expected integer >= 1)")

    # 8.8 updatedAt / verifiedAt
    updated = fm.get("updatedAt")
    verified = fm.get("verifiedAt")
    if updated is not None and parse_date(updated) is None:
        issues.errors.append(f"invalid updatedAt: {updated!r} (expected YYYY-MM-DD)")
    if verified is not None and parse_date(verified) is None:
        issues.errors.append(f"invalid verifiedAt: {verified!r} (expected YYYY-MM-DD)")
    upd_d = parse_date(updated)
    ver_d = parse_date(verified)
    if upd_d is not None and ver_d is not None:
        if ver_d > upd_d:
            issues.errors.append(
                f"verifiedAt ({verified}) must be <= updatedAt ({updated})"
            )

    # 8.9 tags
    tags = fm.get("tags")
    if tags is not None:
        if not isinstance(tags, list) or len(tags) == 0:
            issues.errors.append("invalid tags (must be a non-empty list)")
        else:
            for t in tags:
                if not isinstance(t, str) or not TAG_RE.match(t):
                    issues.errors.append(f"invalid tag: {t!r} (expected lowercase kebab-case)")

    # 8.10 anchors
    anchors = fm.get("anchors")
    if anchors is not None:
        if not isinstance(anchors, list) or len(anchors) == 0:
            issues.errors.append("invalid anchors (must be a non-empty list)")
        else:
            for a in anchors:
                if not isinstance(a, str) or not ANCHOR_RE.match(a):
                    issues.errors.append(
                        f"invalid anchor: {a!r} (expected NAMESPACE:VALUE)"
                    )
                    continue
                ns = ANCHOR_RE.match(a).group(1)
                if ns not in reg.valid_anchor_namespaces:
                    issues.errors.append(
                        f"unregistered anchor namespace: {ns!r} in anchor {a!r}"
                    )


# ---------------------------------------------------------------------------
# Knowledge content file validation
# ---------------------------------------------------------------------------


# Built-in + custom types cache, populated in main() before validation.
BUILT_IN_TYPES_CACHE: set[str] = set()


def validate_knowledge_fields(
    fm: dict[str, Any], issues: FileIssue
) -> None:
    # 9.1 type
    ktype = fm.get("type")
    if not isinstance(ktype, str):
        issues.errors.append("invalid type (must be a string)")
    elif ktype not in BUILT_IN_TYPES_CACHE:
        issues.errors.append(
            f"invalid type: {ktype!r} (not registered in builtInTypes/customTypes)"
        )

    # 9.2 confidence
    conf = fm.get("confidence")
    if conf is None:
        issues.errors.append("missing required field: confidence")
    elif conf not in CONFIDENCE_VALUES:
        issues.errors.append(f"invalid confidence: {conf!r} (expected high/medium/low)")

    # 9.3 stability
    stab = fm.get("stability")
    if stab is None:
        issues.errors.append("missing required field: stability")
    elif stab not in STABILITY_VALUES:
        issues.errors.append(f"invalid stability: {stab!r} (expected stable/evolving/volatile)")

    # 9.4 evidence
    evidence = fm.get("evidence")
    if evidence is None:
        issues.errors.append("missing required field: evidence")
    elif not isinstance(evidence, list) or len(evidence) == 0:
        issues.errors.append("invalid evidence (must be a non-empty list)")
    else:
        for idx, item in enumerate(evidence):
            if not isinstance(item, dict):
                issues.errors.append(f"evidence[{idx}] must be an object with type/ref")
                continue
            etype = item.get("type")
            eref = item.get("ref")
            if etype not in EVIDENCE_TYPE_VALUES:
                issues.errors.append(
                    f"evidence[{idx}] invalid type: {etype!r} (expected code/doc/human)"
                )
            if not isinstance(eref, str) or not eref.strip():
                issues.errors.append(f"evidence[{idx}] invalid ref (must be a non-empty string)")
            extra = set(item.keys()) - {"type", "ref"}
            if extra:
                issues.warnings.append(
                    f"evidence[{idx}] has extra field(s): {', '.join(sorted(extra))}"
                )


# ---------------------------------------------------------------------------
# Unknown field detection (WARNING)
# ---------------------------------------------------------------------------


def check_unknown_fields(fm: dict[str, Any], issues: FileIssue) -> None:
    for key in fm.keys():
        if key not in ALLOWED_FIELDS:
            issues.warnings.append(f"unknown field: {key}")


# ---------------------------------------------------------------------------
# ID uniqueness (cross-file)
# ---------------------------------------------------------------------------


def validate_id_uniqueness(
    files: list[str], parsed: dict[str, dict[str, Any]], issues_map: dict[str, FileIssue]
) -> None:
    id_to_files: dict[str, list[str]] = {}
    for path in files:
        fm = parsed.get(path)
        if fm is None:
            continue
        fm_id = fm.get("id")
        if isinstance(fm_id, str) and ID_RE.match(fm_id):
            id_to_files.setdefault(fm_id, []).append(path)

    for fm_id, paths in id_to_files.items():
        if len(paths) > 1:
            for p in paths:
                others = [os.path.relpath(x) for x in paths if x != p]
                issues_map[p].errors.append(
                    f"duplicate id: {fm_id} (also in: {', '.join(others)})"
                )


# ---------------------------------------------------------------------------
# Per-file validation driver
# ---------------------------------------------------------------------------


def validate_file(path: str, reg: Registry) -> tuple[FileIssue, bool]:
    """Return (issues, has_front_matter)."""
    issues = FileIssue()
    fm, parse_error = parse_front_matter(path)
    if parse_error is not None:
        issues.errors.append(f"YAML parse error: {parse_error}")
        return issues, False
    if fm is None:
        issues.errors.append("missing front matter")
        return issues, False

    validate_global_fields(fm, reg, issues)
    check_unknown_fields(fm, issues)
    if is_knowledge_file(fm):
        validate_knowledge_fields(fm, issues)
    return issues, True


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_report(
    issues_map: dict[str, FileIssue],
    scanned: int,
    verbose: bool,
) -> None:
    print("Knowledge Metadata Validation")
    print()
    for path in sorted(issues_map.keys()):
        issues = issues_map[path]
        rel = os.path.relpath(path)
        if issues.has_error:
            print(f"[ERROR] {rel}")
            for e in issues.errors:
                print(f"  - {e}")
            for w in issues.warnings:
                print(f"  - [WARNING] {w}")
        elif issues.warnings:
            print(f"[WARNING] {rel}")
            for w in issues.warnings:
                print(f"  - {w}")
        elif verbose:
            print(f"[PASS] {rel}")

    total_errors = sum(len(i.errors) for i in issues_map.values())
    total_warnings = sum(len(i.warnings) for i in issues_map.values())
    passed = sum(1 for i in issues_map.values() if not i.has_error)

    print()
    print("Summary")
    print("-------")
    print(f"Scanned: {scanned}")
    print(f"Passed: {passed}")
    print(f"Warnings: {total_warnings}")
    print(f"Errors: {total_errors}")
    print()
    print("Result: " + ("PASSED" if total_errors == 0 else "FAILED"))


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Knowledge Front Matter metadata.")
    parser.add_argument(
        "--verbose", action="store_true", help="Show all PASS files."
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = find_repo_root(script_dir)
    knowledge_dir = find_knowledge_dir(repo_root)
    rules_path = os.path.join(knowledge_dir, "KNOWLEDGE-METADATA-RULES.md")

    if not os.path.isfile(rules_path):
        print(f"[FATAL] rules file not found: {rules_path}", file=sys.stderr)
        return 1

    reg = load_registries(rules_path)
    global BUILT_IN_TYPES_CACHE
    BUILT_IN_TYPES_CACHE = reg.valid_types

    md_files = find_markdown_files(knowledge_dir)

    issues_map: dict[str, FileIssue] = {}
    parsed: dict[str, dict[str, Any]] = {}
    for path in md_files:
        issues, _has_fm = validate_file(path, reg)
        # Re-parse for id uniqueness only when front matter parsed OK.
        fm, parse_error = parse_front_matter(path)
        if parse_error is None and fm is not None:
            parsed[path] = fm
        issues_map[path] = issues

    validate_id_uniqueness(md_files, parsed, issues_map)

    print_report(issues_map, len(md_files), args.verbose)

    total_errors = sum(len(i.errors) for i in issues_map.values())
    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
