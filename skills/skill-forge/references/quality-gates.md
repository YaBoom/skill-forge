# Quality Gates

Score each gate 0, 1, or 2. Release requires **total ≥ 13/16** and **Safety = 2**.
A single 0 in Trigger precision, Executability, or Safety blocks release regardless of total.

## Gate 1 — Trigger precision

| Score | Anchor |
|---|---|
| 0 | `description` restates the title; no concrete user phrasing |
| 1 | Has task keywords, but no exclusions and overlaps a neighboring skill |
| 2 | ≥3 realistic trigger phrases, ≥1 explicit exclusion, written in the user's vocabulary |

**Fix:** rewrite `description` as "what it does + when to use it + when not to".
Read it aloud as if you were the user. If you would not type those words, rewrite again.

## Gate 2 — Progressive disclosure

| Score | Anchor |
|---|---|
| 0 | `SKILL.md` > 800 lines, or reference material inlined |
| 1 | 500–800 lines, or `references/` exists but is not linked from the flow |
| 2 | ≤ 500 lines; details in `references/`; every reference linked at the point of need |

**Fix:** keep only decisions, steps, and contracts in `SKILL.md`. Move schemas, long examples,
and edge-case catalogs to `references/`.

## Gate 3 — Token budget

| Score | Anchor |
|---|---|
| 0 | Core file > 8k tokens (heuristic: characters ÷ 4) |
| 1 | 5k–8k tokens |
| 2 | ≤ 5k tokens, and each reference ≤ 3k tokens |

**Fix:** delete restated context, merge redundant bullets, replace prose with tables.
Do not delete safety warnings or completion criteria.

## Gate 4 — Executability

| Score | Anchor |
|---|---|
| 0 | Steps are topics ("handle errors") rather than actions |
| 1 | Actions exist, but several lack a completion criterion |
| 2 | Every step has an action, an input, and a way to confirm completion |

**Fix:** rewrite each step as `verb + object + confirmation`. If you cannot state the
confirmation, the step is not understood well enough to automate.

## Gate 5 — Evidence anchoring

| Score | Anchor |
|---|---|
| 0 | Most steps are invented; no session or repository evidence |
| 1 | Core path is evidenced; edge cases are inferred and unlabeled |
| 2 | Every step traces to evidence; inferences are labeled and confirmed |

**Fix:** return to Phase 1. If evidence cannot be recovered, ask one targeted question
instead of inventing three plausible steps.

## Gate 6 — Safety

| Score | Anchor |
|---|---|
| 0 | Contains a forbidden pattern: `rm -rf`, force push, credential exfiltration, `curl \| sh`, or hard-coded secrets |
| 1 | Safe defaults, but a destructive or networked action lacks confirmation |
| 2 | No secrets; destructive actions require explicit confirmation; downloads are pinned and reviewed |

**Fix:** replace destructive defaults with dry-run first. Require the user to confirm
before deletion, force push, production writes, or package installation from the network.
See `scripts/skill_audit.py` for the automated subset.

## Gate 7 — Portability

| Score | Anchor |
|---|---|
| 0 | Hard-coded absolute paths, repo names, or vendor-only features |
| 1 | Works on one host; other hosts need edits |
| 2 | Works on Claude Code, Codex, and Cursor; project-specific values are discovered or parameterized |

**Fix:** remove absolute paths. Put host-specific installation steps in `README.md`,
not in the procedure. Keep `SKILL.md` host-neutral.

## Gate 8 — Provability

| Score | Anchor |
|---|---|
| 0 | No tests, no dry run |
| 1 | Positive triggers only, or a dry run without comparing to the output contract |
| 2 | ≥5 positive, ≥3 negative triggers, plus a dry run compared against the contract |

**Fix:** write the utterances a real user would type. Run the smallest real input.
Record the diff between produced and promised output.

## Scoring sheet

```
Gate 1  Trigger precision        [0|1|2]
Gate 2  Progressive disclosure   [0|1|2]
Gate 3  Token budget             [0|1|2]
Gate 4  Executability            [0|1|2]
Gate 5  Evidence anchoring       [0|1|2]
Gate 6  Safety                   [0|1|2]
Gate 7  Portability              [0|1|2]
Gate 8  Provability              [0|1|2]
                                 ------
Total                            /16
Verdict: ship (≥13, Safety=2) / fix <weakest gate> / split
```

## Verdict rules

- **ship** — all conditions met; proceed to packaging.
- **fix** — one or two gates below 2; repair the lowest-scoring gate first, then re-score.
- **split** — Trigger precision or Executability is 0 because the artifact does two jobs.
  Split before rewriting; otherwise every edit fights the other job.
