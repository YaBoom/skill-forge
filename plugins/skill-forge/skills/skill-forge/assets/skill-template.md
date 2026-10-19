---
name: <skill-name>
description: <What it does in one sentence>. Use when <trigger 1>, <trigger 2>, or <trigger 3>; do not use when <exclusion>.
license: MIT
---

# <Skill Name>

<One sentence describing the outcome this skill produces.>

## When to use

- <Concrete situation 1>
- <Concrete situation 2>

Do not use when:

- <Near-miss situation>
- <Out-of-scope task>

## Preconditions

| Input | Required | How to obtain | If missing |
|---|---|---|---|
| <file / env var / service> | yes | <discovery command> | stop and ask |
| <optional input> | no | <default> | use default |

## Workflow

### 1. <Action>

Run `<command or tool call>`. Done when <mechanical completion criterion>.

### 2. <Action>

<Instruction>. Done when <criterion>.

### 3. <Decision>

If <condition A>, do <branch A>. Otherwise do <branch B>. Record which branch was taken.

## Failure handling

| Failure | Signal | Recovery |
|---|---|---|
| <common failure> | <error text or state> | <recovery action> |
| <edge case> | <signal> | <recovery action> |

## Verification

- <mechanical check 1>
- <mechanical check 2>

Do not report success unless both checks pass.

## Output contract

Produce:

1. `<file or message>` with `<required fields>`.
2. `<summary>` containing `<fields>`.

## References

- `references/<topic>.md` — read when <condition>.
