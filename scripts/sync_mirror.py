#!/usr/bin/env python3
"""Mirror the canonical plugin skill into the top-level skills/ directory.

skills.sh and manual installers discover top-level skills/, while Claude Code and
Codex load the plugin payload under plugins/<name>/skills/. Keep one canonical copy
and mirror it before every release.

Usage:
    python scripts/sync_mirror.py
    python scripts/sync_mirror.py --check
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "plugins" / "skill-forge" / "skills" / "skill-forge"
TARGET = REPO_ROOT / "skills" / "skill-forge"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".DS_Store")


def compare(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    if not right.exists():
        return [f"missing target: {right.relative_to(REPO_ROOT)}"]

    left_files = {p.relative_to(left) for p in left.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
    right_files = {p.relative_to(right) for p in right.rglob("*") if p.is_file() and "__pycache__" not in p.parts}

    for missing in sorted(left_files - right_files):
        problems.append(f"missing in mirror: {missing}")
    for extra in sorted(right_files - left_files):
        problems.append(f"extra in mirror: {extra}")
    for relative in sorted(left_files & right_files):
        if not filecmp.cmp(left / relative, right / relative, shallow=False):
            problems.append(f"content differs: {relative}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync or verify the skills/ mirror.")
    parser.add_argument("--check", action="store_true", help="verify without writing")
    args = parser.parse_args()

    if not SOURCE.is_dir():
        print(f"error: canonical skill not found: {SOURCE}", file=sys.stderr)
        return 2

    if args.check:
        problems = compare(SOURCE, TARGET)
        if problems:
            for problem in problems:
                print(f"[DRIFT] {problem}")
            print("\nrun: python scripts/sync_mirror.py")
            return 1
        print("mirror is in sync")
        return 0

    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SOURCE, TARGET, ignore=IGNORE)
    print(f"synced {SOURCE.relative_to(REPO_ROOT)} -> {TARGET.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
