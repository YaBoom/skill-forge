# Distillation Playbook

Use this when Phase 1 evidence exists but the workflow is still tangled in one project's
details. The goal is a procedure that survives a change of repository, machine, and author.

## 1. Extraction questions

Answer these in order. Stop when every answer traces to evidence.

### Trigger

- What did the user literally type or click right before the successful run?
- What state existed that made this the right action? (failing test, new release, incident, review request)
- What near-miss situations should *not* activate this skill?

### Inputs

- Which files, branches, environment variables, or services were required?
- Which of them can be discovered automatically, and which must be provided?
- What happens if one is missing — stop, ask, or fall back?

### Steps

- List every command, edit, and check in execution order.
- For each step, write the completion criterion: how do we know it finished?
- Mark steps that were retried or that failed first. Those are your failure modes.

### Decisions

- Where did the run branch? What signal drove the branch?
- Which branch is the common case, and which is the exception?

### Failure modes

- What error appeared, and what actually fixed it?
- Which fix was a workaround rather than a root-cause repair? Label it.

### Verification

- What proves the outcome is correct, independent of the agent's own claim?
- Prefer mechanical checks: exit codes, test results, diff shape, schema validation, HTTP status.

### Output contract

- Exactly which files or messages are produced?
- What are the required fields, formats, and naming rules?
- What must *not* be produced?

## 2. De-projectivization rules

| Leak | Replace with |
|---|---|
| `/Users/<user>/work/<repo>` | "the repository root" + a discovery command |
| `acme-api`, `acme-web` | `<service-name>` variable |
| Customer or tenant names | `<tenant>` placeholder |
| One-off version numbers | "the version declared in `<manifest>`" |
| Personal API keys | "the credential from `<env var>`" |
| Internal URLs | "the base URL from `<config key>`" |
| Alice's shell alias | The underlying command |

Rule of thumb: if the sentence cannot be understood by a competent engineer who has never
seen the original repository, it is not portable yet.

## 3. Split or keep

Split the workflow when any of these is true:

- Two independent outcomes are produced (for example "review" and "deploy").
- Two different trigger situations exist.
- One half needs credentials and the other does not.
- The combined `SKILL.md` exceeds 500 lines even after moving detail to `references/`.

Keep it as one skill when the second half is only meaningful as verification of the first.

## 4. Worked example

### Raw evidence

> In `acme-api`, tests failed because `DATABASE_URL` pointed to staging. I ran
> `docker compose up -d db`, exported `DATABASE_URL=postgres://localhost:5432/acme_test`,
> ran `pnpm db:migrate`, then `pnpm test -- --runInBand`. It passed. Then I opened
> `src/db/pool.ts` and bumped the pool size from 5 to 20 because CI kept timing out.

### Distilled

**Trigger:** integration tests fail against a local or staging database, or CI times out
while acquiring a connection.

**Inputs:** repository root, Docker, the project's package manager, a test database name.

**Steps:**

1. Start the local database with the repository's compose file. Done when the health check passes.
2. Point the test environment at the local database. Done when the connection string resolves to localhost.
3. Run migrations. Done when the migration command exits 0.
4. Run the test suite serially. Done when the suite exits 0.
5. If CI still times out, inspect the connection pool configuration. Change one setting at a time,
   rerun, and record the result.

**Decision:** serial execution is the common case; parallel execution only after the pool is sized.

**Failure mode:** a stale exported variable in the shell overrides the `.env` file — verify the
effective value, not the file.

**Verification:** exit code 0 from the suite plus a log line showing the local database host.

**Output contract:** a passing test run and a short note naming the changed configuration key.

Note what disappeared: `acme-api`, `pnpm`, `src/db/pool.ts`, and the number 20. The package
manager becomes "the project's package manager"; the pool setting becomes "the connection pool
configuration". A skill that keeps those details only works for one repository.

## 5. Redaction checklist

Before writing the final file, scan for:

- API keys, tokens, passwords, private keys, cookies.
- Customer names, email addresses, internal hostnames.
- Absolute home or workspace paths.
- Proprietary business rules that should not be published.

Redact, then confirm with the user before publishing outside the organization.
