# Skill Scorecard — <skill-name>

## 1. Verdict

| Field | Value |
|---|---|
| Total | <n>/16 |
| Safety gate | <0/1/2> |
| Verdict | ship / fix / split |
| Blocking gate | <gate name or none> |
| Auditor | skill-forge v1.0.0 |

## 2. Gates

| # | Gate | Score | Evidence |
|---|---|---|---|
| 1 | Trigger precision | /2 | <trigger phrases found, exclusions> |
| 2 | Progressive disclosure | /2 | <SKILL.md lines, references linked> |
| 3 | Token budget | /2 | <estimated tokens> |
| 4 | Executability | /2 | <steps with completion criteria> |
| 5 | Evidence anchoring | /2 | <sources; inferred steps> |
| 6 | Safety | /2 | <audit findings> |
| 7 | Portability | /2 | <hosts tested; leaks removed> |
| 8 | Provability | /2 | <tests and dry run> |

## 3. Evidence ledger

| Signal | Source | Reusable | Notes |
|---|---|---|---|
| <session action / command / diff / file> | <source> | yes/no | <why it matters> |

Redactions applied: <list>
Pending inferences: <list or none>

## 4. File tree

```
<skill-name>/
├── SKILL.md
├── references/<file>.md
├── assets/<file>.md
└── scripts/<file>.py
```

## 5. Trigger tests

### Positive

| # | User utterance | Expected |
|---|---|---|
| 1 | <utterance> | activates |
| 2 | <utterance> | activates |
| 3 | <utterance> | activates |
| 4 | <utterance> | activates |
| 5 | <utterance> | activates |

### Negative

| # | User utterance | Expected |
|---|---|---|
| 1 | <near miss> | does not activate |
| 2 | <near miss> | does not activate |
| 3 | <near miss> | does not activate |

### Dry run

| Item | Produced | Contract | Match |
|---|---|---|---|
| <artifact> | <what appeared> | <what was promised> | yes/no |

## 6. Publish plan

| Channel | Command or action | Owner | Manual step |
|---|---|---|---|
| Local | `cp -r . ~/.claude/skills/<name>` | author | restart host |
| skills.sh | `npx skills add <owner>/<repo> -s <name>` | author | push repo |
| Claude directory | submit via claude.com/marketplace | <user> | login + form |
| Codex plugins | pull request to `openai/plugins` | <user> | login + review |

Rollback: <how to unpublish or revert the version>
