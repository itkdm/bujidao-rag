#!/usr/bin/env python3
"""Knowledge Metadata Report generator (read-only statistics).

Reads Front Matter from Knowledge Markdown files (already validated by
``validate_metadata.py``) and produces a read-only statistics report. This
script NEVER modifies any file and never writes a report file.

Usage:
    python knowledge/scripts/metadata_report.py [--app CODE] [--type T] [--today YYYY-MM-DD]

Exit codes:
    0  -> report generated successfully
    1  -> metadata validation has ERRORs, report not generated
    2  -> CLI argument error (unknown appCode / type)
"""

from __future__ import annotations

import argparse
import os
import sys
from collections import Counter, defaultdict
from datetime import date, datetime
from typing import Any

from metadata_utils import (
    SCOPE_VALUES,
    STATUS_VALUES,
    CONFIDENCE_VALUES,
    STABILITY_VALUES,
    EVIDENCE_TYPE_VALUES,
    Registry,
    find_knowledge_dir,
    find_repo_root,
    find_rules_path,
    is_knowledge_file,
    load_registries,
    parse_date,
    parse_front_matter,
)

# Fixed ordering for status / confidence / stability reporting.
STATUS_ORDER = ["OFFICIAL", "CANDIDATE", "DRAFT", "DEPRECATED"]
CONFIDENCE_ORDER = ["high", "medium", "low"]
STABILITY_ORDER = ["stable", "evolving", "volatile"]
EVIDENCE_ORDER = ["code", "doc", "human"]
SCOPE_ORDER = ["global", "app", "cross-app"]


def sorted_by_count(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Sort (key, count) by count desc, then key asc for stable output."""
    return sorted(items, key=lambda kv: (-kv[1], kv[0]))


def fmt_pct(count: int, total: int) -> str:
    if total == 0:
        return "0.0%"
    return f"{count * 100.0 / total:.1f}%"


def load_documents(knowledge_dir: str) -> list[tuple[str, dict[str, Any]]]:
    """Return list of (rel_path, front_matter) for scannable markdown files."""
    from metadata_utils import find_markdown_files

    docs: list[tuple[str, dict[str, Any]]] = []
    for path in find_markdown_files(knowledge_dir):
        fm, parse_error = parse_front_matter(path)
        if parse_error is not None or fm is None:
            # Skip files the validator would report; report uses validated data only.
            continue
        docs.append((os.path.relpath(path), fm))
    return docs


def run_validation_first() -> bool:
    """Run the validator logic; return True if no ERROR exists (warnings ok)."""
    import importlib.util

    validator_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_metadata.py")
    spec = importlib.util.spec_from_file_location("validate_metadata", validator_path)
    if spec is None or spec.loader is None:
        return False
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = find_repo_root(script_dir)
    knowledge_dir = find_knowledge_dir(repo_root)
    rules_path = find_rules_path(knowledge_dir)
    if not os.path.isfile(rules_path):
        print(f"[FATAL] rules file not found: {rules_path}", file=sys.stderr)
        sys.exit(1)

    reg = load_registries(rules_path)
    mod.BUILT_IN_TYPES_CACHE = reg.valid_types
    md_files = mod.find_markdown_files(knowledge_dir)

    parsed: dict[str, dict[str, Any]] = {}
    issues_map: dict[str, Any] = {}
    for path in md_files:
        issues, _ = mod.validate_file(path, reg)
        fm, perr = parse_front_matter(path)
        if perr is None and fm is not None:
            parsed[path] = fm
        issues_map[path] = issues

    mod.validate_id_uniqueness(md_files, parsed, issues_map)
    total_errors = sum(len(i.errors) for i in issues_map.values())
    return total_errors == 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Knowledge metadata report.")
    parser.add_argument("--app", help="Restrict to a specific appCode.")
    parser.add_argument("--type", help="Restrict to a specific knowledge type.")
    parser.add_argument(
        "--today",
        help="Override 'today' date (YYYY-MM-DD) for verification-age buckets.",
    )
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = find_repo_root(script_dir)
    knowledge_dir = find_knowledge_dir(repo_root)
    rules_path = find_rules_path(knowledge_dir)

    if not os.path.isfile(rules_path):
        print(f"[FATAL] rules file not found: {rules_path}", file=sys.stderr)
        return 1

    reg = load_registries(rules_path)

    # Filter arguments validation.
    if args.app is not None and args.app not in reg.app_codes:
        print(f"Unknown appCode: {args.app}")
        print("Available appCodes: " + (", ".join(sorted(reg.app_codes)) or "(none)"))
        return 2
    if args.type is not None and args.type not in reg.valid_types:
        print(f"Unknown type: {args.type}")
        print("Available types: " + (", ".join(sorted(reg.valid_types)) or "(none)"))
        return 2

    # Prerequisite: run validation first.
    if not run_validation_first():
        print("Metadata validation failed.")
        print("Run:")
        print("python knowledge/scripts/validate_metadata.py")
        return 1

    # Determine "today".
    if args.today:
        today = parse_date(args.today)
        if today is None:
            print(f"Invalid --today value: {args.today!r} (expected YYYY-MM-DD)")
            return 2
    else:
        today = date.today()

    docs = load_documents(knowledge_dir)

    # Apply filters.
    if args.app is not None:
        docs = [d for d in docs if d[1].get("appCode") == args.app]
    if args.type is not None:
        docs = [d for d in docs if d[1].get("type") == args.type]

    print_report(docs, reg, today, args.app, args.type)
    return 0


def print_report(
    docs: list[tuple[str, dict[str, Any]]],
    reg: Registry,
    today: date,
    app_filter: str | None,
    type_filter: str | None,
) -> None:
    total = len(docs)
    knowledge_docs = [(p, fm) for p, fm in docs if is_knowledge_file(fm)]
    infra_docs = [(p, fm) for p, fm in docs if not is_knowledge_file(fm)]
    n_knowledge = len(knowledge_docs)
    n_infra = len(infra_docs)

    print("Knowledge Metadata Report")
    print("=========================")
    print()

    # Filters
    print("Filters")
    print("-------")
    print(f"AppCode: {app_filter if app_filter else 'ALL'}")
    print(f"Type:    {type_filter if type_filter else 'ALL'}")
    print()

    # Overview
    apps_represented = {fm.get("appCode") for _, fm in docs if fm.get("appCode")}
    print("Overview")
    print("--------")
    print(f"Documents:              {total}")
    print(f"Knowledge files:        {n_knowledge}")
    print(f"Infrastructure files:    {n_infra}")
    print(f"Apps represented:        {len(apps_represented)}")
    print()

    # By Scope
    print("By Scope")
    print("--------")
    scope_counter = Counter(fm.get("scope", "(missing)") for _, fm in docs)
    for key in SCOPE_ORDER:
        if key in scope_counter:
            print(f"{key:<10}{scope_counter[key]}")
    for key, cnt in sorted_by_count(
        [(k, c) for k, c in scope_counter.items() if k not in SCOPE_ORDER]
    ):
        print(f"{key:<10}{cnt}")
    print()

    # By AppCode
    if app_filter is None:
        print("By AppCode")
        print("----------")
        app_counter = Counter(fm.get("appCode") for _, fm in docs if fm.get("appCode"))
        for key, cnt in sorted_by_count(list(app_counter.items())):
            print(f"{key:<22}{cnt}")
        print(f"Apps represented: {len(app_counter)}")
        print()

    # By Type (knowledge files only)
    if type_filter is None:
        print("By Type")
        print("-------")
        type_counter = Counter(fm.get("type") for _, fm in knowledge_docs)
        for key, cnt in sorted_by_count(list(type_counter.items())):
            print(f"{key:<22}{cnt}")
        print()

    # By Status (with percentage)
    print("By Status")
    print("---------")
    status_counter = Counter(fm.get("status", "(missing)") for _, fm in docs)
    for key in STATUS_ORDER:
        if key in status_counter:
            cnt = status_counter[key]
            print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, total)}")
    for key, cnt in sorted_by_count(
        [(k, c) for k, c in status_counter.items() if k not in STATUS_ORDER]
    ):
        print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, total)}")
    print()

    # By Owner
    print("By Owner")
    print("--------")
    owner_counter = Counter(fm.get("owner") for _, fm in docs if fm.get("owner"))
    for key, cnt in sorted_by_count(list(owner_counter.items())):
        print(f"{key:<22}{cnt}")
    print()

    # By Maintainer
    print("By Maintainer")
    print("-------------")
    maint_counter = Counter()
    for _, fm in docs:
        for m in fm.get("maintainers", []) or []:
            if isinstance(m, str):
                maint_counter[m] += 1
    for key, cnt in sorted_by_count(list(maint_counter.items())):
        print(f"{key:<22}{cnt}")
    print(f"Maintainers represented: {len(maint_counter)}")
    print()

    # By Confidence (knowledge files only; always shown, uses filtered set)
    print("By Confidence")
    print("-------------")
    conf_counter = Counter(fm.get("confidence") for _, fm in knowledge_docs)
    for key in CONFIDENCE_ORDER:
        if key in conf_counter:
            cnt = conf_counter[key]
            print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, n_knowledge)}")
    for key, cnt in sorted_by_count(
        [(k, c) for k, c in conf_counter.items() if k not in CONFIDENCE_ORDER]
    ):
        print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, n_knowledge)}")
    print()

    # By Stability (knowledge files only; always shown, uses filtered set)
    print("By Stability")
    print("------------")
    stab_counter = Counter(fm.get("stability") for _, fm in knowledge_docs)
    for key in STABILITY_ORDER:
        if key in stab_counter:
            cnt = stab_counter[key]
            print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, n_knowledge)}")
    for key, cnt in sorted_by_count(
        [(k, c) for k, c in stab_counter.items() if k not in STABILITY_ORDER]
    ):
        print(f"{key:<10}{cnt:<5}{fmt_pct(cnt, n_knowledge)}")
    print()

    # Evidence Type Usage (knowledge files only; always shown, uses filtered set)
    print("Evidence Type Usage")
    print("-------------------")
    entry_counter = Counter()
    doc_using = defaultdict(set)
    for p, fm in knowledge_docs:
        for item in fm.get("evidence", []) or []:
            if isinstance(item, dict):
                et = item.get("type")
                if et in EVIDENCE_TYPE_VALUES:
                    entry_counter[et] += 1
                    doc_using[et].add(p)
    for key in EVIDENCE_ORDER:
        if key in entry_counter:
            print(f"{key:<8}{entry_counter[key]:<5}entries   {len(doc_using[key])} docs")
    print()

    # Verification Age
    print("Verification Age")
    print("----------------")
    buckets = {"0-30 days": 0, "31-90 days": 0, "91-180 days": 0, ">180 days": 0}
    oldest: list[tuple[date, str]] = []
    for p, fm in docs:
        vd = parse_date(fm.get("verifiedAt"))
        if vd is None:
            continue
        delta = (today - vd).days
        if delta <= 30:
            buckets["0-30 days"] += 1
        elif delta <= 90:
            buckets["31-90 days"] += 1
        elif delta <= 180:
            buckets["91-180 days"] += 1
        else:
            buckets[">180 days"] += 1
        oldest.append((vd, p))
    for label in ["0-30 days", "31-90 days", "91-180 days", ">180 days"]:
        print(f"{label:<12}{buckets[label]}")
    oldest.sort(key=lambda x: x[0])
    print()
    print("Oldest verification:")
    if oldest:
        for vd, p in oldest[:5]:
            print(f"  {vd.isoformat()}  {p}")
    else:
        print("  (none)")
    print()

    # Cross-stats only when no --type filter (these break down by type).
    if type_filter is None:
        # AppCode × Type
        print("AppCode x Type")
        print("--------------")
        cross: dict[str, Counter] = defaultdict(Counter)
        for _, fm in knowledge_docs:
            ac = fm.get("appCode")
            if not ac:
                continue
            t = fm.get("type")
            if t:
                cross[ac][t] += 1
        for ac in sorted(cross.keys()):
            print(ac)
            for t, cnt in sorted_by_count(list(cross[ac].items())):
                print(f"  {t:<20}{cnt}")
            print()

        # Status × Confidence (knowledge files)
        print("Status x Confidence")
        print("-------------------")
        scross: dict[str, Counter] = defaultdict(Counter)
        for _, fm in knowledge_docs:
            st = fm.get("status")
            cf = fm.get("confidence")
            if st and cf:
                scross[st][cf] += 1
        for st in STATUS_ORDER:
            if st in scross:
                print(st)
                for cf, cnt in sorted_by_count(list(scross[st].items())):
                    print(f"  {cf:<20}{cnt}")
                print()


if __name__ == "__main__":
    sys.exit(main())
