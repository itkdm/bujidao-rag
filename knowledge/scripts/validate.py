#!/usr/bin/env python3
"""运行当前仓库的知识库、研发文档与归档结构校验。"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "workspace",
        nargs="?",
        help="工作区根目录；默认从当前脚本位置自动定位",
    )
    git_group = parser.add_mutually_exclusive_group()
    git_group.add_argument(
        "--git-staged",
        action="store_true",
        help="同时检查暂存区中的归档移动映射",
    )
    git_group.add_argument(
        "--git-range",
        metavar="BASE..HEAD",
        help="同时检查指定提交范围中的归档移动映射",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    default_workspace = Path(__file__).resolve().parents[2]
    workspace = Path(args.workspace).resolve() if args.workspace else default_workspace
    validator = (
        workspace
        / ".agents"
        / "skills"
        / "knowledge-docs-initializer"
        / "scripts"
        / "validate_initialization.py"
    )
    if not validator.is_file():
        print(f"错误：缺少知识库校验器：{validator}", file=sys.stderr)
        return 2

    command = [sys.executable, str(validator), str(workspace)]
    if args.git_staged:
        command.append("--git-staged")
    elif args.git_range:
        command.extend(("--git-range", args.git_range))
    completed = subprocess.run(
        command,
        cwd=workspace,
        check=False,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
