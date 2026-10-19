---
name: sync-skill-mirror
description: Keep a plugin's canonical skill directory and the repository-level skills/ mirror identical before release. Use when a repository stores one canonical copy under plugins/<name>/skills/ and a second copy under skills/ for skills.sh or manual installers; use before tagging a release, after editing SKILL.md or its references, or when an installer reports stale content. Do not use for repositories that already have a single source of truth or for syncing unrelated directories.
license: MIT
---

# Sync Skill Mirror

Prevent a published skill from drifting away from the copy that hosts actually load.

## When to use

- A repository keeps `plugins/<name>/skills/<skill>/` as canonical and `skills/<skill>/` as a mirror.
- `SKILL.md`, `references/`, `assets/`, or `scripts/` changed.
- A release is about to be tagged.
- An installer reports content that does not match the repository.

Do not use when the repository has only one copy, or when the two directories are
intentionally different.

## Preconditions

| Input | Required | How to obtain | If missing |
|---|---|---|---|
| Repository root | yes | `git rev-parse --show-toplevel` | stop |
| Canonical skill path | yes | `plugins/*/skills/*/SKILL.md` | stop and ask which copy is canonical |
| Mirror path | yes | `skills/<skill-name>/` | create it from the canonical copy |

Confirm which copy is canonical before writing. If both copies have diverged, compare
the last commit that touched each one and ask the user which version wins.

## Workflow

### 1. Compare

Run the repository's sync script in check mode:

```bash
python scripts/sync_mirror.py --check
```

Done when the command exits with either `0` (in sync) or `1` with a list of drift items.
Record the drift list; it is the evidence for the release note.

### 2. Resolve direction

If the canonical copy is newer, mirror forward. If the mirror contains a hotfix that the
canonical copy lacks, stop: merge the hotfix into the canonical copy first, then mirror.
Never edit the mirror directly.

### 3. Mirror

```bash
python scripts/sync_mirror.py
```

Done when the command reports the source and target paths.

### 4. Verify

```bash
python scripts/sync_mirror.py --check
```

Done when it prints `mirror is in sync`.

### 5. Audit both copies

```bash
python plugins/<name>/skills/<skill>/scripts/skill_audit.py \
  plugins/<name>/skills/<skill> --repo .
```

Done when the audit exits `0`. If the mirror was created by copying, the audit result
applies to both copies; rerun it only if the copies differ.

## Failure handling

| Failure | Signal | Recovery |
|---|---|---|
| Wrong canonical copy | Drift reverses after mirroring | Restore from git, confirm the source, rerun |
| Untracked files in the mirror | `extra in mirror` | Delete the extra files, never copy them back |
| Script missing | `canonical skill not found` | Fix the path constants or run from the repository root |
| Symlinked directories | Copy fails or loops | Replace symlinks with real files before releasing |

## Verification

- `sync_mirror.py --check` exits 0.
- `skill_audit.py` exits 0 on the canonical copy.
- `git status` shows changes only in the intended directories.

## Output contract

Produce:

1. A drift report listing every file that differed before the sync.
2. A confirmation that the mirror check exits 0 after the sync.
3. A one-line release note naming the skill version and the files that changed.

## References

- The repository-level sync script (`sync_mirror.py`) — its compare and copy implementation.
