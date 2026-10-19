# skill-forge

A Claude Code and Codex plugin that turns a completed workflow into a tested,
publish-ready Agent Skill.

## What it does

- Harvests evidence from the current session, git history, and project files.
- Distills the workflow into seven reusable elements.
- Scores the result against eight quality gates.
- Generates `SKILL.md`, references, assets, and optional scripts.
- Produces trigger tests and a dry-run record.
- Packages the skill for Claude Code, Codex, Cursor, and skills.sh.

## Install

Claude Code:

```bash
/plugin marketplace add YaBoom/skill-forge
/plugin install skill-forge@skill-forge-marketplace
```

Codex:

```bash
cp -r skills/skill-forge ~/.codex/skills/
```

skills.sh:

```bash
npx skills add YaBoom/skill-forge -s skill-forge -g -y
```

## Use

```text
Turn what we just finished into a reusable skill.
Audit my SKILL.md and tell me why it never triggers.
Package this skill for Claude Code and Codex.
```

## Audit

```bash
python skills/skill-forge/scripts/skill_audit.py skills/skill-forge --repo ../..
```

Exit code 0 means no blocking findings.

## License

MIT
