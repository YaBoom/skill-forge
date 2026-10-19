# Skill Forge

[![preflight](https://github.com/YaBoom/skill-forge/actions/workflows/preflight.yml/badge.svg)](https://github.com/YaBoom/skill-forge/actions/workflows/preflight.yml)
[![license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Turn a workflow you just finished into a tested, publish-ready Agent Skill.

Skill Forge is not another prompt template. It harvests evidence from the current session,
git history, and project files; distills it into a portable procedure; scores it against
eight quality gates; and packages the result for Claude Code, Codex, Cursor, and skills.sh.

## Why this exists

Most skills are written from imagination. They describe what the author *thinks* the
workflow is, then fail to trigger, leak project-specific paths, or collapse when the
repository changes.

The most-installed skills in the ecosystem win for a different reason: they are either
entry points (`find-skills`), verifiable deliverables (`frontend-design`), or a
subscribable methodology (`mattpocock/skills`). Skill Forge targets the gap none of them
fill — **turning a real, completed workflow into a distributable asset**.

## Install

Claude Code, from this repository as a marketplace:

```bash
/plugin marketplace add YaBoom/skill-forge
/plugin install skill-forge@skill-forge-marketplace
```

Codex:

```bash
git clone https://github.com/YaBoom/skill-forge.git
cp -r skill-forge/plugins/skill-forge/skills/skill-forge ~/.codex/skills/
```

Any Agent Skills host via skills.sh:

```bash
npx skills add YaBoom/skill-forge -s skill-forge -g -y
```

Manual install:

```bash
cp -r plugins/skill-forge/skills/skill-forge ~/.claude/skills/
```

Restart the host and confirm the skill appears in `/skills` or `$` completion.

## Use

Ask for the outcome, not the mechanism:

- "Turn what we just did into a reusable skill."
- "This migration took three hours. Make it repeatable."
- "My SKILL.md never triggers. Audit it and fix the description."
- "Package this skill for Claude Code and Codex, then tell me how to publish it."

Skill Forge runs six phases:

| Phase | Output |
|---|---|
| 0. Classify | Skill / command / subagent / plugin / MCP — and why |
| 1. Harvest | Evidence ledger with sources and redactions |
| 2. Distill | Seven elements: trigger, inputs, steps, decisions, failures, verification, output |
| 3. Gate | Eight-gate scorecard, release threshold 13/16 with Safety = 2 |
| 4. Generate | `SKILL.md`, `references/`, `assets/`, `scripts/` |
| 5. Prove | ≥5 positive and ≥3 negative trigger tests, plus a dry run |
| 6. Ship | README, Claude and Codex manifests, publish plan |

Every run returns five artifacts: scorecard, evidence ledger, file tree, trigger tests,
and a publish plan with the one manual step the user must perform.

## The eight gates

| # | Gate | What it prevents |
|---|---|---|
| 1 | Trigger precision | A skill nobody can find |
| 2 | Progressive disclosure | A 900-line wall of text |
| 3 | Token budget | A skill that eats the context window |
| 4 | Executability | Vague advice instead of steps |
| 5 | Evidence anchoring | Invented procedures |
| 6 | Safety | Destructive commands and leaked secrets |
| 7 | Portability | A skill that only works in the author's repo |
| 8 | Provability | "It works on my machine" |

Run the deterministic subset before publishing:

```bash
python plugins/skill-forge/skills/skill-forge/scripts/skill_audit.py \
  plugins/skill-forge/skills/skill-forge --repo .
```

Exit code 0 means no blocking findings. The manual gates still require a human review.

## Repository layout

```
.
├── .claude-plugin/marketplace.json      # Claude Code marketplace
├── .agents/plugins/marketplace.json     # Codex marketplace
├── plugins/skill-forge/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   ├── README.md
│   └── skills/skill-forge/              # canonical skill
│       ├── SKILL.md
│       ├── references/
│       ├── assets/
│       └── scripts/
├── skills/skill-forge/                  # mirror for skills.sh and manual installs
├── docs/market-analysis.md              # market data and positioning rationale
└── scripts/sync_mirror.py               # keeps the mirror in sync
```

## Publishing

Three channels, in order:

1. **Local** — copy into `~/.claude/skills` or `~/.codex/skills`.
2. **skills.sh** — push to GitHub, then `npx skills add <owner>/<repo> -s skill-forge`.
3. **Official directories** — submit the Claude plugin via `claude.com/marketplace`,
   or open a pull request against `openai/plugins` for Codex.

The detailed manifest formats and submission checklist live in
[`references/publish-playbook.md`](plugins/skill-forge/skills/skill-forge/references/publish-playbook.md).

## Design principles

- Evidence over imagination.
- One skill, one job.
- Trigger before content.
- Progressive disclosure.
- Ship the package, not the prompt.

## License

MIT. See [LICENSE](LICENSE).
