#!/usr/bin/env python3
"""Repository pre-flight check for Skill Forge.

Validates manifests, marketplace sources, the skills/ mirror, and the canonical
skill audit in one pass.

Usage:
    python scripts/preflight.py
"""

from __future__ import annotations

import filecmp
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "plugins" / "skill-forge" / "skills" / "skill-forge"
MIRROR = ROOT / "skills" / "skill-forge"
AUDIT = CANONICAL / "scripts" / "skill_audit.py"

results: list[tuple[bool, str, str]] = []


def check(condition: bool, name: str, detail: str = "") -> None:
    results.append((condition, name, detail))


def load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        check(False, f"json: {path.relative_to(ROOT)}", str(exc))
        return None


def main() -> int:
    required = [
        ROOT / "README.md",
        ROOT / "LICENSE",
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
        ROOT / "plugins" / "skill-forge" / ".claude-plugin" / "plugin.json",
        ROOT / "plugins" / "skill-forge" / ".codex-plugin" / "plugin.json",
        CANONICAL / "SKILL.md",
    ]
    for path in required:
        check(path.exists(), f"exists: {path.relative_to(ROOT)}")

    claude_market = load_json(ROOT / ".claude-plugin" / "marketplace.json")
    if claude_market:
        for entry in claude_market.get("plugins", []):
            source = entry.get("source")
            if isinstance(source, str):
                target = (ROOT / source).resolve()
                check(target.exists(), f"claude marketplace source: {source}")

    codex_market = load_json(ROOT / ".agents" / "plugins" / "marketplace.json")
    if codex_market:
        for entry in codex_market.get("plugins", []):
            source = entry.get("source", {})
            if isinstance(source, dict) and source.get("source") == "local":
                target = (ROOT / source.get("path", "")).resolve()
                check(target.exists(), f"codex marketplace source: {source.get('path')}")

    for manifest in [ROOT / "plugins" / "skill-forge" / ".claude-plugin" / "plugin.json",
                     ROOT / "plugins" / "skill-forge" / ".codex-plugin" / "plugin.json"]:
        data = load_json(manifest)
        if data:
            label = manifest.parent.parent.name
            check(data.get("name") == "skill-forge", f"plugin name: {label}")
            check(data.get("version") == "1.0.0", f"plugin version: {label}")

    codex_plugin = load_json(ROOT / "plugins" / "skill-forge" / ".codex-plugin" / "plugin.json")
    if codex_plugin:
        skills_path = codex_plugin.get("skills")
        check(bool(skills_path), "codex manifest declares skills")
        if skills_path:
            check((ROOT / "plugins" / "skill-forge" / skills_path).exists(), "codex skills path exists")

    check(MIRROR.exists(), "skills/ mirror exists")
    if MIRROR.exists():
        left = {p.relative_to(CANONICAL) for p in CANONICAL.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        right = {p.relative_to(MIRROR) for p in MIRROR.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
        check(left == right, "mirror file set matches", f"only-canonical={sorted(left - right)} only-mirror={sorted(right - left)}")
        differing = [str(rel) for rel in sorted(left & right) if not filecmp.cmp(CANONICAL / rel, MIRROR / rel, shallow=False)]
        check(not differing, "mirror content matches", ", ".join(differing))

    if AUDIT.exists():
        completed = subprocess.run(
            [sys.executable, str(AUDIT), str(CANONICAL), "--repo", str(ROOT), "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        check(completed.returncode == 0, "skill audit exits 0", completed.stderr.strip())
        if completed.stdout.strip():
            try:
                report = json.loads(completed.stdout)
                score = report.get("score", {})
                results.append((
                    score.get("auto_total") == score.get("auto_max"),
                    "automatic gates 10/10",
                    f"{score.get('auto_total')}/{score.get('auto_max')}",
                ))
            except json.JSONDecodeError:
                check(False, "audit output is valid JSON")

    width = max(len(name) for _, name, _ in results) + 2
    failed = 0
    for ok, name, detail in results:
        if not ok:
            failed += 1
        status = "PASS" if ok else "FAIL"
        suffix = f"  {detail}" if detail and not ok else ""
        print(f"[{status}] {name.ljust(width)}{suffix}")

    print("")
    print(f"{len(results) - failed}/{len(results)} checks passed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
