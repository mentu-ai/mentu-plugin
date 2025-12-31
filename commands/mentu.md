---
description: Mentu commitment ledger - track work with evidence
---

# Mentu Command

You have access to the Mentu commitment ledger via the `mentu` CLI.

## Available Actions

| Command | Description |
|---------|-------------|
| `mentu status` | Show current commitments |
| `mentu status --mine` | Show your claimed commitments |
| `mentu capture "text"` | Record an observation |
| `mentu commit "task" --source mem_xxx` | Create commitment |
| `mentu claim cmt_xxx` | Take responsibility |
| `mentu submit cmt_xxx --summary "..."` | Submit for review |
| `mentu log` | Show operation history |

## Workflow

1. At session start, check `mentu status --mine` for claimed work
2. When completing work, capture evidence then submit
3. Never close directly — use submit for review

Run the appropriate mentu command based on user request.
