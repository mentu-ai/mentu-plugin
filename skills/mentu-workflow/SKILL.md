---
name: mentu-workflow
description: Automatically track work as Mentu commitments when user indicates trackable tasks
---

# Mentu Workflow Skill

When the user indicates work that should be tracked (phrases like "track this", "create a commitment", "I need to do", "add to my tasks"):

## Workflow

1. **Capture the observation**
   ```bash
   mentu capture "User request: <description>" --kind task
   ```

2. **Create commitment**
   ```bash
   mentu commit "<actionable deliverable>" --source <memory_id>
   ```

3. **Claim immediately**
   ```bash
   mentu claim <commitment_id>
   ```

4. **On completion, submit with evidence**
   ```bash
   mentu capture "Completed: <what was done>" --kind evidence
   mentu submit <commitment_id> --summary "<one line summary>" --include-files
   ```

## Evidence Requirements

Every submission must include:
- What was done (specific actions)
- Verifiable artifacts (file paths, test results, etc.)
- Connection to original request

## Session Start

At session start, always check for existing commitments:
```bash
mentu status --mine
```

Resume work on any claimed commitments before taking new ones.

## On Rejection

If your submission is rejected:

1. Run `mentu show cmt_xxx` to see rejection reason
2. Use `/rewind` to restore code to a working state
3. Address the feedback
4. Submit again with new evidence

### Recovery Limitations

Claude Code's `/rewind` only tracks Edit/Write tool operations. The following are NOT recoverable via /rewind:

| Operation | Recoverable? | Alternative |
|-----------|--------------|-------------|
| Edit tool | Yes | /rewind |
| Write tool | Yes | /rewind |
| Bash file ops (rm, mv, cp) | No | Manual cleanup |
| Git commands | No | git reset/checkout |
| npm install/uninstall | No | Re-run commands |

Mentu's PostToolUse hook captures ALL operations as evidence, even those /rewind cannot recover.
