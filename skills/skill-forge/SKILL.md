---
name: skill-forge
description: Distill a workflow the user just completed into a production-ready Agent Skill, or upgrade an existing skill for distribution. Use when the user asks to create a skill from this session, repository, runbook, SOP, command history, or a repeated task; when a one-off success should become reusable; or when an existing SKILL.md needs sharper triggering, token-budget review, security audit, plugin packaging, or submission to Claude Code, Codex, Cursor, or skills.sh. Do not use for one-off prompts, MCP server implementation, or simply installing a third-party skill.
license: MIT
---

# Skill Forge

Turn evidence into a skill. A skill is not a longer prompt — it is a tested, versioned
asset that another agent can load and execute without the original author present.

Default behavior: **harvest first, ask second**. Only ask the user when a required
fact cannot be recovered from the session, repository, or command history.

## When to use this skill

Use it when any of these is true:

- The user says "make this a skill", "沉淀一下", "turn this into a skill", "save this workflow".
- A task just succeeded and the user wants it repeatable.
- An existing `SKILL.md` under-triggers, over-triggers, is too long, or leaks project-specific paths.
- The user wants to publish to Claude Code, Codex, Cursor, or skills.sh.

Do **not** use it for:

- Writing a one-off prompt (just write the prompt).
- Building an MCP server or a full application (use the relevant engineering skill).
- Copying a third-party skill into the local directory (use the installer).

## Operating principles

1. **Evidence over imagination.** Every step must trace to something that actually ran:
   a tool call, a diff, a command, a file, or an explicit user statement. Mark inferred steps.
2. **One skill, one job.** If the workflow has two independent outcomes, split it.
3. **Trigger before content.** A perfect skill that never fires is worthless. Spend disproportionate
   effort on `description` and negative triggers.
4. **Progressive disclosure.** `SKILL.md` holds the decision flow. Long procedures, schemas, and
   examples go to `references/` and are read only when needed.
5. **Ship the package, not the prompt.** A publishable skill includes the file tree, manifests,
   trigger tests, and a scorecard.

## Workflow

### Phase 0 — Classify the artifact

Before writing, decide what the user actually needs:

| Signal | Artifact | Why |
|---|---|---|
| Reusable procedure, triggered by task context | **Skill** | Model decides when to load it |
| User-invoked action with arguments | **Command** | Explicit `/name` invocation |
| Isolated context or parallel work | **Subagent** | Separate context window |
| Bundle of skills + commands + hooks + MCP | **Plugin** | Single install unit |
| External API, auth, or persistent service | **MCP server** | Skills cannot hold credentials safely |

If the answer is not a Skill, say so and route to the right artifact. Do not force everything into `SKILL.md`.

### Phase 1 — Harvest evidence

Build an **Evidence Ledger** before writing any instruction:

| Signal | Source | Reusable? | Why it matters |
|---|---|---|---|
| … | session / git diff / shell history / file / user statement | yes/no | … |

Collect from, in priority order:

1. The current session: what was attempted, what failed, what finally worked.
2. `git log --oneline -20`, `git diff`, and changed file paths.
3. Shell history and repeated commands.
4. Project files: `README`, `Makefile`, CI config, runbooks, `AGENTS.md`, `CLAUDE.md`.
5. The user's own description, used only to fill gaps.

Rules:

- If a step was never executed, label it `INFERRED` and require user confirmation.
- If the evidence contains secrets, tokens, customer names, or private URLs, redact them
  before they reach `SKILL.md`.
- Stop harvesting when every step of the procedure has a source.

### Phase 2 — Distill the workflow

Reduce the ledger to seven elements. Write them down before drafting:

1. **Trigger** — the concrete situation that should activate the skill, in the user's words.
2. **Inputs** — what must exist before step 1 (files, env vars, credentials, repo state).
3. **Steps** — ordered actions, each with a completion criterion.
4. **Decision points** — branches, and the condition for each branch.
5. **Failure modes** — what commonly breaks, and the recovery action.
6. **Verification** — how to prove the skill worked, not just that it ran.
7. **Output contract** — exact files, formats, and fields produced.

Then **de-projectivize**: replace repository names, absolute paths, customer names, and
one-off values with variables or discovery steps. A skill that only works in the author's
repo will not survive distribution.

See `references/distillation-playbook.md` for the full extraction checklist and examples.

### Phase 3 — Pass the quality gates

Score all eight gates from 0 to 2 using `references/quality-gates.md`.

| Gate | Pass condition |
|---|---|
| 1. Trigger precision | `description` contains ≥3 real trigger phrases and ≥1 exclusion |
| 2. Progressive disclosure | `SKILL.md` ≤ 500 lines; long material moved to `references/` |
| 3. Token budget | Core `SKILL.md` ≤ 5k tokens by heuristic |
| 4. Executability | Every step has an action and a completion criterion |
| 5. Evidence anchoring | No `INFERRED` step left unconfirmed |
| 6. Safety | No destructive commands, secrets, or unreviewed network installs |
| 7. Portability | Works for Claude Code, Codex, and Cursor without project-private values |
| 8. Provability | ≥5 positive and ≥3 negative trigger tests, plus a dry run |

**Release threshold: total ≥ 13/16 and Safety = 2.** Below threshold, fix the weakest gate
instead of adding more prose.

Run the bundled audit:

```bash
python scripts/skill_audit.py <path-to-skill-directory>
```

Treat a non-zero exit code as a blocker. The script checks frontmatter, naming, line and
token budget, broken relative links, dangerous command patterns, and manifest consistency.

### Phase 4 — Generate the package

Use `assets/skill-template.md` as the skeleton. Produce:

```
<skill-name>/
├── SKILL.md                 # required, decision flow only
├── references/              # optional, loaded on demand
│   └── <topic>.md
├── assets/                  # optional, templates the skill fills in
│   └── <template>.md
└── scripts/                 # optional, deterministic operations
    └── <tool>.py
```

Naming rules:

- `name` is lowercase, hyphenated, and identical to the directory name.
- Verb-first when the skill performs an action (`audit-*`, `forge-*`, `migrate-*`).
- No vendor prefixes unless the skill is vendor-specific.

Writing rules:

- Use imperative sentences. "Run X. Confirm Y." not "You might want to consider X."
- Prefer a table or a numbered list over paragraphs.
- Put the most common path first; move edge cases to `references/`.
- Reference files with relative paths from the skill root, never absolute paths.
- State what to do when a precondition is missing.

### Phase 5 — Prove it fires

Write trigger tests into the scorecard:

- **Positive (≥5):** realistic user utterances that must activate the skill.
- **Negative (≥3):** near-miss utterances that must NOT activate it.
- **Dry run:** execute the workflow on the smallest real input available, and record
  what was produced versus the output contract.

If a positive test fails, rewrite `description`. If a negative test fails, add an explicit
exclusion to `description` or move the overlapping content out of this skill.

### Phase 6 — Package and ship

Generate the distribution layer only after Phase 5 passes:

- `README.md` with install commands for each host.
- `.claude-plugin/plugin.json` for Claude Code.
- `.codex-plugin/plugin.json` for Codex.
- Marketplace entries when publishing a repository.
- A publish plan naming the channel, reviewer, and rollback step.

See `references/publish-playbook.md` for the exact file contents and the three release
channels (skills.sh, Claude directory, Codex plugins repository).

## Output contract

Every completed run must return these five items, in this order:

1. **Scorecard** — eight gates, total, and verdict (`ship` / `fix` / `split`).
2. **Evidence Ledger** — signals used, redactions applied, inferences pending.
3. **File tree** — every generated file with a one-line purpose.
4. **Trigger tests** — positive and negative utterances with expected routing.
5. **Publish plan** — channel, exact commands, and the one thing the user must do manually.

If the skill cannot pass the gates, return the scorecard and the blocking gate instead of
claiming completion.

## Anti-patterns

| Anti-pattern | Symptom | Fix |
|---|---|---|
| Prompt in disguise | Long prose, no steps, no verification | Add decision points and a completion criterion per step |
| Trigger sprawl | `description` lists every possible use | Keep 3–5 real triggers; add exclusions |
| Project leakage | Hard-coded paths, repo names, customer data | Replace with discovery steps and variables |
| Reference dump | 800-line `SKILL.md` | Move detail to `references/`, keep the decision flow |
| Unsafe automation | Forbidden patterns such as `curl \| sh`, `rm -rf`, unquoted variables | Require explicit confirmation; use safe defaults |
| Orphan skill | No install path, no README, no tests | Complete Phase 5 and Phase 6 |

## References

- `references/distillation-playbook.md` — extraction questions, de-projectivization, examples.
- `references/quality-gates.md` — rubric, scoring anchors, and failure remedies.
- `references/publish-playbook.md` — manifests, marketplace entries, submission steps.
- `assets/skill-template.md` — copy-ready skeleton.
- `assets/scorecard-template.md` — report format for the output contract.
- `scripts/skill_audit.py` — deterministic pre-flight audit.
