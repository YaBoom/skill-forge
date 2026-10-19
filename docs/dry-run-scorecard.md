# Dry Run Scorecard — sync-skill-mirror

This is the worked example referenced by Skill Forge Phase 5. The input was a real
workflow executed in this repository: mirroring the canonical plugin skill into the
top-level `skills/` directory and verifying the result.

It is an author-run example, not an independent benchmark.

## 1. Verdict

| Field | Value |
|---|---|
| Skill | `examples/sync-skill-mirror` |
| Total | 16/16 |
| Safety gate | 2/2 |
| Verdict | ship |
| Blocking gate | none |
| Auditor | skill-forge v1.0.0 |

## 2. Gates

| # | Gate | Score | Evidence |
|---|---|---|---|
| 1 | Trigger precision | 2/2 | Three concrete triggers (release, edited SKILL.md, installer reports stale content) and one exclusion (single source of truth) |
| 2 | Progressive disclosure | 2/2 | 103 lines; no reference material inlined |
| 3 | Token budget | 2/2 | ~890 tokens, below the 5k core budget |
| 4 | Executability | 2/2 | Five steps, each with a command and an exit condition |
| 5 | Evidence anchoring | 2/2 | Derived from `scripts/sync_mirror.py` and two real runs in this session |
| 6 | Safety | 2/2 | No deletion of source data; mirror only; no secrets or network installs |
| 7 | Portability | 2/2 | Paths discovered from the repository root; no absolute paths |
| 8 | Provability | 2/2 | Five positive and three negative triggers below; dry run executed twice (drift, then in sync) |

## 3. Evidence ledger

| Signal | Source | Reusable | Notes |
|---|---|---|---|
| Canonical path `plugins/skill-forge/skills/skill-forge` | repository tree | yes | Became the source parameter |
| Mirror path `skills/skill-forge` | repository tree | yes | Became the target parameter |
| First run created the mirror | session command output | yes | Proves the write path |
| Second run printed `mirror is in sync` | session command output | yes | Proves the verification step |
| `--check` exit code 1 on drift | `sync_mirror.py` implementation | yes | Defines the drift signal |

Redactions applied: absolute Windows workspace path replaced with "repository root".
Pending inferences: none.

## 4. File tree

```
sync-skill-mirror/
└── SKILL.md      # decision flow, steps, failure handling, output contract
```

## 5. Trigger tests

### Positive

| # | User utterance | Expected |
|---|---|---|
| 1 | "I edited SKILL.md, sync the mirror before we tag." | activates |
| 2 | "The installed skill looks stale, check the mirror." | activates |
| 3 | "Run the pre-release sync check." | activates |
| 4 | "skills/ and plugins/ differ, fix it." | activates |
| 5 | "Verify the mirror is identical before publishing." | activates |

### Negative

| # | User utterance | Expected |
|---|---|---|
| 1 | "Sync my fork with upstream." | does not activate |
| 2 | "Copy this directory to another drive." | does not activate |
| 3 | "Publish the skill to skills.sh." | does not activate (routing to publish, not mirror) |

### Dry run

| Item | Produced | Contract | Match |
|---|---|---|---|
| Drift report | `synced ... -> ...` on first run; `mirror is in sync` on the second | drift list + exit 0 | yes |
| Audit | `no findings`, auto score 10/10 | exit 0 | yes |

## 6. Publish plan

| Channel | Command or action | Owner | Manual step |
|---|---|---|---|
| Local | `cp -r examples/sync-skill-mirror ~/.claude/skills/` | author | restart host |
| skills.sh | not published (example only) | — | — |
| Official directories | not submitted (example only) | — | — |

Rollback: delete `examples/sync-skill-mirror`; it is not referenced by any manifest.
