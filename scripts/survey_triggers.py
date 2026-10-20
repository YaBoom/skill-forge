"""Count how many installed agent skills declare a negative trigger.

An agent skill's `description` is the only thing a host sees before deciding
whether to load it. A description that only says what the skill does forces the
host to load it in every superficially similar situation; a description that also
says when *not* to use it lets the host route elsewhere.

This script scans every SKILL.md under the usual agent skill directories, parses
the frontmatter description, and reports how many contain an explicit negative
trigger.

Usage:
    python scripts/survey_triggers.py
    python scripts/survey_triggers.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

NEGATIVE_TRIGGER = re.compile(
    r"(do not use|not for|don't use|avoid using|not intended for)",
    re.IGNORECASE,
)

SKILL_ROOTS = (
    Path.home() / ".claude" / "skills",
    Path.home() / ".agents" / "skills",
    Path.home() / ".cursor" / "skills",
    Path.home() / ".codex" / "skills",
)

DESCRIPTION = re.compile(r"^description:\s*(.+)$", re.MULTILINE | re.IGNORECASE)


def find_skills() -> list[Path]:
    found: set[Path] = set()
    for root in SKILL_ROOTS:
        if not root.is_dir():
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            if "SKILL.md" in filenames:
                found.add(Path(dirpath) / "SKILL.md")
    return sorted(found)


def dedupe_by_name(paths: list[Path]) -> list[Path]:
    """Keep one file per skill name.

    The same skill is routinely installed into several host directories
    (``.claude``, ``.agents``, ``.cursor``, ``.codex``). Counting each copy
    inflates the sample and biases it toward whichever skill was installed the
    most times, so collapse by directory name and keep the first path.
    """
    seen: dict[str, Path] = {}
    for path in paths:
        seen.setdefault(path.parent.name.lower(), path)
    return sorted(seen.values())


def read_description(path: Path) -> str | None:
    """Return the frontmatter description, joining indented continuation lines."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    frontmatter = text[: end if end != -1 else len(text)]
    match = DESCRIPTION.search(frontmatter)
    if not match:
        return None

    parts = [match.group(1)]
    for line in frontmatter[match.end():].splitlines():
        if line.startswith((" ", "\t")) and line.strip():
            parts.append(line.strip())
        else:
            break
    return " ".join(parts)


def classify(path: Path) -> str:
    name = path.parent.name.lower()
    return "azure" if "azure" in name else "other"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    parser.add_argument(
        "--no-dedupe",
        action="store_true",
        help="count every installed copy instead of one per skill name",
    )
    args = parser.parse_args()

    all_files = find_skills()
    skills = all_files if args.no_dedupe else dedupe_by_name(all_files)
    groups: dict[str, list[int]] = {"azure": [0, 0], "other": [0, 0]}
    missing: list[str] = []
    rows: list[dict[str, object]] = []

    for path in skills:
        description = read_description(path)
        if description is None:
            missing.append(str(path))
            continue
        key = classify(path)
        has_trigger = bool(NEGATIVE_TRIGGER.search(description))
        groups[key][0] += 1
        if has_trigger:
            groups[key][1] += 1
        rows.append(
            {
                "skill": path.parent.name,
                "group": key,
                "negative_trigger": has_trigger,
            }
        )

    total = sum(g[0] for g in groups.values())
    with_trigger = sum(g[1] for g in groups.values())

    if args.json:
        print(
            json.dumps(
                {
                    "skill_files": len(all_files),
                    "unique_skills": len(skills),
                    "with_description": total,
                    "with_negative_trigger": with_trigger,
                    "rate": round(with_trigger / total, 4) if total else None,
                    "missing_description": missing,
                    "groups": {
                        key: {
                            "total": counts[0],
                            "with_negative_trigger": counts[1],
                            "rate": round(counts[1] / counts[0], 4) if counts[0] else None,
                        }
                        for key, counts in groups.items()
                    },
                    "skills": rows,
                },
                indent=2,
            )
        )
        return 0

    print(f"SKILL.md files found:        {len(all_files)}")
    print(f"unique skills:               {len(skills)}")
    print(f"with frontmatter description: {total}")
    print(f"contain a negative trigger:   {with_trigger}")
    print(f"do not:                       {total - with_trigger}")
    if total:
        print(f"negative-trigger rate:        {with_trigger / total:.1%}")
    if missing:
        print(f"unparsable frontmatter:       {len(missing)}")
    print()
    for key, (count, triggered) in groups.items():
        rate = f"{triggered / count:.1%}" if count else "n/a"
        print(f"{key:6s} total={count:3d}  with_negative_trigger={triggered:2d}  rate={rate}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
