# Publish Playbook

Three release channels, in ascending order of difficulty. Do not skip L1 and L2 to chase L3.

| Channel | Artifact | Gatekeeper | Time to live |
|---|---|---|---|
| L1 Local | `~/.claude/skills/<name>`, `~/.codex/skills/<name>` | none | minutes |
| L2 skills.sh | public GitHub repo + `npx skills add` | none | same day |
| L3 Official directories | plugin submission / curated repository | Anthropic or OpenAI review | weeks |

---

## L1 — Local install

Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r <skill-name> ~/.claude/skills/
```

Codex:

```bash
mkdir -p ~/.codex/skills
cp -r <skill-name> ~/.codex/skills/
```

Project-scoped alternatives: `.claude/skills/` and `.codex/skills/` at the repository root.
Restart the host after copying. Verify the skill appears in `/skills` or `$` completion.

---

## L2 — skills.sh

Requirements:

- Public GitHub repository.
- At least one directory containing `SKILL.md`, preferably under `skills/<name>/`.
- Valid frontmatter with `name` and `description`.

Install command users will run:

```bash
npx skills add <owner>/<repo> -s <skill-name> -g -y
```

The `-s` flag selects a single skill when the repository contains several. Without it,
the installer may prompt interactively.

Repository layout that works across hosts:

```
<repo>/
├── skills/<skill-name>/SKILL.md      # discovered by skills.sh and generic installers
├── .claude-plugin/marketplace.json   # Claude Code marketplace
├── .agents/plugins/marketplace.json  # Codex marketplace
└── plugins/<plugin-name>/
    ├── .claude-plugin/plugin.json
    ├── .codex-plugin/plugin.json
    └── skills/<skill-name>/          # plugin payload
```

If the plugin payload and the top-level `skills/` directory would duplicate content,
keep one canonical copy and mirror it with a script before each release.

---

## L3a — Claude Code official directory

Entry point: <https://claude.com/marketplace> and the submission form linked from
`anthropics/claude-plugins-official`.

Minimum package:

```
<plugin-name>/
├── .claude-plugin/plugin.json
├── skills/<skill-name>/SKILL.md
└── README.md
```

`plugin.json` (verified against the official example plugin):

```json
{
  "name": "<plugin-name>",
  "description": "<one paragraph, outcome-focused>",
  "version": "1.0.0",
  "author": {
    "name": "<author>",
    "url": "https://github.com/<owner>"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "license": "MIT"
}
```

Rules that cause silent rejection:

- `name` is an immutable slug. Renaming after publication breaks existing installs.
- The plugin must not contain secrets or unreviewed binaries.
- Skills must trigger on their own; reviewers should not need to read the README to use them.

Review flow: submission → automated security scan → human review → publish. Publishing
is manual after approval, so you can choose the release window.

---

## L3b — Codex plugins repository

Entry point: `openai/plugins` (the older `openai/skills` repository is deprecated).

Minimum package:

```
<plugin-name>/
├── .codex-plugin/plugin.json
├── skills/<skill-name>/SKILL.md
└── README.md
```

`plugin.json` (verified against `openai/plugins`):

```json
{
  "name": "<plugin-name>",
  "version": "1.0.0",
  "description": "<one paragraph, outcome-focused>",
  "author": {
    "name": "<author>",
    "url": "https://github.com/<owner>"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "repository": "https://github.com/<owner>/<repo>",
  "license": "MIT",
  "keywords": ["..."],
  "skills": "./skills/",
  "interface": {
    "displayName": "<Display Name>",
    "shortDescription": "<under 80 characters>",
    "longDescription": "<two or three sentences>",
    "developerName": "<author>",
    "category": "Developer Tools",
    "capabilities": ["Interactive", "Read", "Write"],
    "defaultPrompt": [
      "<a sentence a real user would type>"
    ]
  }
}
```

Marketplace entry in `.agents/plugins/marketplace.json`:

```json
{
  "name": "local",
  "source": { "source": "local", "path": "./plugins/<plugin-name>" },
  "policy": { "installation": "AVAILABLE", "authentication": "ON_INSTALL" },
  "category": "Developer Tools"
}
```

`source` may also be `{ "source": "url", "url": "..." }` or
`{ "source": "git-subdir", "url": "...", "path": "..." }` for external repositories.

---

## Submission checklist

Before opening a pull request or submitting a form:

- [ ] `skill_audit.py` exits 0 on the skill directory.
- [ ] `SKILL.md` has ≥3 positive trigger phrases and ≥1 exclusion.
- [ ] No absolute paths, secrets, customer names, or internal URLs.
- [ ] Every relative link in `SKILL.md` resolves.
- [ ] `README.md` includes install, usage, and uninstall instructions.
- [ ] A dry run is recorded with the produced artifact.
- [ ] License file exists and matches the manifest.
- [ ] Version follows semver and is bumped from the previous release.
- [ ] Plugin `name` matches the directory and the marketplace entry.
- [ ] The one manual step (account login, form submission) is written down for the user.

## What not to do

- Do not submit a skill that only works inside your own repository.
- Do not bundle several unrelated skills to inflate the package.
- Do not copy a third-party skill without its license and attribution.
- Do not claim benchmark numbers you cannot reproduce.
- Do not publish credentials, even in examples or test fixtures.
