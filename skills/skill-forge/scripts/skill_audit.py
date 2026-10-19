#!/usr/bin/env python3
"""Deterministic pre-flight audit for Agent Skills.

Usage:
    python skill_audit.py <skill-directory>
    python skill_audit.py <skill-directory> --json
    python skill_audit.py <skill-directory> --repo <repository-root>

Exit codes:
    0  no blocking findings
    1  at least one blocking finding
    2  invalid input
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"`((?:references|assets|scripts)/[^`\s]+)`")
TOKEN_CHARS = 4
MAX_CORE_LINES = 500
MAX_CORE_TOKENS = 5000
MAX_REF_TOKENS = 3000

DANGEROUS_PATTERNS = [
    ("destructive-delete", re.compile(r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r")),
    ("force-push", re.compile(r"git\s+push[^\n]*--force")),
    ("pipe-to-shell", re.compile(r"(?:curl|wget)[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh")),
    ("sql-drop", re.compile(r"\bDROP\s+(?:TABLE|DATABASE)\b", re.I)),
    ("secret-openai", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}")),
    ("secret-github", re.compile(r"\bghp_[A-Za-z0-9]{20,}")),
    ("secret-aws", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("secret-slack", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
]

SAFE_CONTEXT = (
    "anti-pattern", "anti pattern", "do not", "don't", "never", "avoid",
    "forbidden", "blocked", "must not", "prohibited",
)

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"/Users/[A-Za-z0-9._-]+"),
    re.compile(r"/home/[A-Za-z0-9._-]+"),
    re.compile(r"[A-Za-z]:\\\\Users\\\\"),
    re.compile(r"/workspace/"),
]


class Finding:
    def __init__(self, level: str, code: str, message: str) -> None:
        self.level = level
        self.code = code
        self.message = message

    def as_dict(self) -> dict:
        return {"level": self.level, "code": self.code, "message": self.message}


def parse_frontmatter(text: str) -> dict | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    data: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // TOKEN_CHARS)


def read_text(path: Path, findings: list[Finding]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        findings.append(Finding("error", "encoding", f"{path.name} is not UTF-8"))
        return ""
    except OSError as exc:
        findings.append(Finding("error", "io", f"cannot read {path.name}: {exc}"))
        return ""


def audit_skill(skill_dir: Path) -> dict:
    findings: list[Finding] = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_dir.is_dir():
        findings.append(Finding("error", "missing-dir", f"not a directory: {skill_dir}"))
        return build_result(skill_dir, findings, {}, None)
    if not skill_md.is_file():
        findings.append(Finding("error", "missing-skill", "SKILL.md not found"))
        return build_result(skill_dir, findings, {}, None)

    text = read_text(skill_md, findings)
    lines = text.count("\n") + 1
    core_tokens = estimate_tokens(text)
    frontmatter = parse_frontmatter(text)

    if frontmatter is None:
        findings.append(Finding("error", "frontmatter", "missing or malformed YAML frontmatter"))
        frontmatter = {}

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")

    if not name:
        findings.append(Finding("error", "name", "frontmatter is missing 'name'"))
    elif not KEBAB_RE.match(name):
        findings.append(Finding("error", "name-format", f"'name' must be kebab-case, got '{name}'"))
    elif name != skill_dir.name:
        findings.append(Finding(
            "error", "name-mismatch",
            f"'name' is '{name}' but directory is '{skill_dir.name}'",
        ))

    if not description:
        findings.append(Finding("error", "description", "frontmatter is missing 'description'"))
    else:
        if len(description) < 60:
            findings.append(Finding("warn", "description-short", "description looks too short to trigger reliably"))
        if len(description) > 1024:
            findings.append(Finding("warn", "description-long", "description exceeds 1024 characters"))
        if "use when" not in description.lower() and "use this" not in description.lower():
            findings.append(Finding("warn", "description-trigger", "description has no explicit 'Use when ...' clause"))
        if not any(token in description.lower() for token in ("do not use", "not use when", "don't use", "exclude")):
            findings.append(Finding("warn", "description-exclusion", "description has no exclusion clause"))

    if lines > MAX_CORE_LINES:
        findings.append(Finding(
            "error", "length",
            f"SKILL.md has {lines} lines (limit {MAX_CORE_LINES}); move detail to references/",
        ))
    elif lines > MAX_CORE_LINES * 0.8:
        findings.append(Finding("warn", "length-near", f"SKILL.md has {lines} lines, close to the limit"))

    if core_tokens > MAX_CORE_TOKENS:
        findings.append(Finding(
            "error", "tokens",
            f"SKILL.md is ~{core_tokens} tokens (limit {MAX_CORE_TOKENS})",
        ))

    for linked in LINK_RE.findall(text):
        target = skill_dir / linked
        if not target.exists():
            findings.append(Finding("error", "broken-link", f"referenced path does not exist: {linked}"))
        elif target.is_file() and target.suffix == ".md":
            ref_tokens = estimate_tokens(read_text(target, findings))
            if ref_tokens > MAX_REF_TOKENS:
                findings.append(Finding(
                    "warn", "ref-tokens",
                    f"{linked} is ~{ref_tokens} tokens (target ≤{MAX_REF_TOKENS})",
                ))

    scan_files = [skill_md] + sorted(skill_dir.glob("references/**/*.md")) + sorted(skill_dir.glob("assets/**/*.md"))
    scan_files += [p for p in sorted(skill_dir.glob("scripts/**/*")) if p.is_file() and p.name != Path(__file__).name]

    for path in scan_files:
        content = read_text(path, findings) if path.suffix in {".md", ".py", ".sh", ".json", ".yaml", ".yml"} else ""
        if not content:
            continue
        in_fence = False
        for number, line in enumerate(content.splitlines(), start=1):
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            lowered = line.lower()
            if any(marker in lowered for marker in SAFE_CONTEXT):
                continue
            executable = path.suffix != ".md" or in_fence
            for code, pattern in DANGEROUS_PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(
                        "error" if executable else "warn", code,
                        f"{path.relative_to(skill_dir)}:{number} matches {code}",
                    ))
            for pattern in ABSOLUTE_PATH_PATTERNS:
                if pattern.search(line):
                    findings.append(Finding(
                        "warn", "absolute-path",
                        f"{path.relative_to(skill_dir)}:{number} contains an absolute path",
                    ))
                    break

    readme_candidates = [skill_dir / "README.md", skill_dir.parent / "README.md", skill_dir.parent.parent / "README.md"]
    if not any(path.exists() for path in readme_candidates):
        findings.append(Finding("warn", "readme", "no README.md in the skill or plugin directory"))
    if not any((parent / "LICENSE").exists() for parent in [skill_dir, *skill_dir.parents]):
        findings.append(Finding("warn", "license", "no LICENSE file found in any parent directory"))

    metadata = {
        "name": name,
        "lines": lines,
        "tokens": core_tokens,
        "references": sorted(p.name for p in skill_dir.glob("references/*.md")),
    }
    return build_result(skill_dir, findings, metadata, frontmatter)


def score(findings: list[Finding], metadata: dict, frontmatter: dict | None) -> dict:
    levels = [f.level for f in findings]
    codes = {f.code for f in findings}
    description = (frontmatter or {}).get("description", "").lower()

    trigger = 2
    if "description-trigger" in codes or "description-short" in codes:
        trigger = 1
    if "description" in codes:
        trigger = 0
    if "description-exclusion" in codes and trigger == 2:
        trigger = 1

    disclosure = 2
    if "length-near" in codes or "ref-tokens" in codes:
        disclosure = 1
    if "length" in codes:
        disclosure = 0

    budget = 2 if "tokens" not in codes else 0

    unsafe_codes = {"destructive-delete", "force-push", "pipe-to-shell", "sql-drop"}
    safety = 2
    if any(f.level == "error" and (f.code.startswith("secret-") or f.code in unsafe_codes) for f in findings):
        safety = 0
    elif any(f.code.startswith("secret-") or f.code in unsafe_codes or f.code == "absolute-path" for f in findings):
        safety = 1

    portability = 2 if "absolute-path" not in codes else 1

    return {
        "trigger_precision": trigger,
        "progressive_disclosure": disclosure,
        "token_budget": budget,
        "safety": safety,
        "portability": portability,
        "auto_total": trigger + disclosure + budget + safety + portability,
        "auto_max": 10,
        "manual_gates": ["executability", "evidence_anchoring", "provability"],
        "release_blocked": "error" in levels or safety == 0,
    }


def build_result(skill_dir: Path, findings: list[Finding], metadata: dict, frontmatter: dict | None) -> dict:
    return {
        "skill": str(skill_dir),
        "ok": not any(f.level == "error" for f in findings),
        "findings": [f.as_dict() for f in findings],
        "metadata": metadata,
        "score": score(findings, metadata, frontmatter),
    }


def audit_repo(repo_root: Path) -> list[Finding]:
    findings: list[Finding] = []
    claude_market = repo_root / ".claude-plugin" / "marketplace.json"
    codex_market = repo_root / ".agents" / "plugins" / "marketplace.json"

    for path in (claude_market, codex_market):
        if not path.is_file():
            findings.append(Finding("warn", "marketplace-missing", f"missing {path.relative_to(repo_root)}"))
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("error", "marketplace-json", f"{path.name}: {exc}"))
            continue
        for entry in data.get("plugins", []):
            source = entry.get("source")
            if isinstance(source, str):
                target = (repo_root / source).resolve()
            elif isinstance(source, dict) and source.get("source") == "local":
                target = (repo_root / source.get("path", "")).resolve()
            else:
                continue
            if not target.exists():
                findings.append(Finding(
                    "error", "marketplace-source",
                    f"{path.name}: plugin '{entry.get('name')}' points to missing path {source}",
                ))

    for manifest_path in sorted(repo_root.glob("plugins/*/.claude-plugin/plugin.json")):
        plugin_dir = manifest_path.parent.parent
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("error", "plugin-json", f"{manifest_path}: {exc}"))
            continue
        if data.get("name") != plugin_dir.name:
            findings.append(Finding(
                "error", "plugin-name",
                f"{plugin_dir.name}/.claude-plugin/plugin.json name is '{data.get('name')}'",
            ))
        if not (plugin_dir / "skills").is_dir():
            findings.append(Finding("warn", "plugin-skills", f"{plugin_dir.name} has no skills/ directory"))

    for manifest_path in sorted(repo_root.glob("plugins/*/.codex-plugin/plugin.json")):
        plugin_dir = manifest_path.parent.parent
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(Finding("error", "plugin-json", f"{manifest_path}: {exc}"))
            continue
        if data.get("name") != plugin_dir.name:
            findings.append(Finding(
                "error", "plugin-name",
                f"{plugin_dir.name}/.codex-plugin/plugin.json name is '{data.get('name')}'",
            ))
        skills = data.get("skills")
        if not skills:
            findings.append(Finding("warn", "codex-skills", f"{plugin_dir.name} manifest has no 'skills' field"))
        elif not (plugin_dir / skills).exists():
            findings.append(Finding("error", "codex-skills", f"{plugin_dir.name} skills path does not exist: {skills}"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit an Agent Skill before publishing.")
    parser.add_argument("skill_dir", type=Path, help="path to the skill directory")
    parser.add_argument("--repo", type=Path, default=None, help="repository root to validate manifests")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    if not args.skill_dir.exists():
        print(f"error: {args.skill_dir} does not exist", file=sys.stderr)
        return 2

    result = audit_skill(args.skill_dir.resolve())
    if args.repo:
        repo_findings = audit_repo(args.repo.resolve())
        result["findings"].extend(f.as_dict() for f in repo_findings)
        result["ok"] = result["ok"] and not any(f.level == "error" for f in repo_findings)
        if any(f.level == "error" for f in repo_findings):
            result["score"]["release_blocked"] = True

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["ok"] else 1

    print(f"skill: {result['skill']}")
    print(f"lines: {result['metadata'].get('lines', '?')}  tokens: ~{result['metadata'].get('tokens', '?')}")
    print("")
    if result["findings"]:
        for finding in result["findings"]:
            print(f"[{finding['level'].upper():5}] {finding['code']}: {finding['message']}")
    else:
        print("no findings")

    scored = result["score"]
    print("")
    print(f"auto score: {scored['auto_total']}/{scored['auto_max']} (gates 1,2,3,6,7)")
    print(f"manual gates still required: {', '.join(scored['manual_gates'])}")
    print(f"verdict: {'BLOCKED' if scored['release_blocked'] else 'PASS (pending manual gates)'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
