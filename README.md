# Mentu Plugin for Claude Code

The Commitment Ledger — accountability for AI agents.

## Installation

### From Marketplace (Recommended)

1. Add the Mentu marketplace:
   ```
   /plugin marketplace add mentu-ai/mentu-plugin
   ```

2. Install the plugin:
   ```
   /plugin install mentu
   ```

That's it! The plugin is now active.

### Local Development

```bash
git clone https://github.com/mentu-ai/mentu-plugin
claude --plugin-dir ./mentu-plugin
```

## Prerequisites

- **mentu-cli**: Install globally with `npm install -g mentu-cli`
- **Mentu workspace**: Run `mentu init` in your project

## Commands

| Command | Description |
|---------|-------------|
| `/mentu:mentu` | Main command with subcommand dispatch |
| `/mentu:commit "message"` | Quick-create commitment |
| `/mentu:claim cmt_xxx` | Claim commitment |
| `/mentu:submit cmt_xxx` | Submit for review |
| `/mentu:status` | Show current state |

## How It Works

```
+---------------------------------------------------------------------+
|                    MENTU WORKFLOW                                    |
+---------------------------------------------------------------------+

SessionStart -----> Inject claimed commitments into context
                   "You have 2 open commitments..."

PostToolUse  -----> Capture Edit/Write/Bash as evidence
(automatic)        "Captured mem_xxx: Modified auth.ts"

Stop -------------> Enforce commitment closure
(if enabled)       "Cannot stop: cmt_xxx still open"
```

### SessionStart Hook

When you start Claude Code, the plugin checks for your claimed commitments and injects them into the conversation context. This ensures agents resume work where they left off.

### PostToolUse Hook

Every Edit, Write, or Bash operation is automatically captured as evidence in the Mentu ledger. No manual tracking required.

### Stop Hook

When `--mentu-enforcer` is active, agents cannot stop until their claimed commitments are closed with evidence.

## Team Setup

Add to your project's `.claude/settings.json`:

```json
{
  "plugins": {
    "marketplaces": ["mentu-ai/mentu-plugin"],
    "installed": ["mentu@mentu-ai"]
  }
}
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MENTU_ACTOR` | Your actor identity (e.g., `agent:claude-code`) |
| `MENTU_ENFORCER` | Set to `true` to enforce commitment closure |

## Skill: mentu-workflow

The plugin includes a skill that auto-activates when you say things like:
- "track this task"
- "create a commitment"
- "add to my tasks"

It automatically captures -> commits -> claims -> submits.

## Agents

| Agent | Purpose |
|-------|---------|
| `commitment-validator` | Validates evidence sufficiency before closure |
| `triage-agent` | Classifies observations into actionable items |

## The Three Rules

1. **Commitments trace to memories** — every obligation has an origin
2. **Closure requires evidence** — proving done, not marking done
3. **Append-only** — nothing edited, nothing deleted

## Recovery

When a commitment is rejected:

```bash
# 1. View rejection reason
mentu show cmt_xxx

# 2. Restore code (Claude Code)
# Press Esc twice or use /rewind

# 3. Address feedback and resubmit
mentu submit cmt_xxx --summary "Addressed feedback: ..."
```

**Tip**: /rewind recovers Edit/Write changes. Bash operations require manual cleanup.

## Git-Backed Recovery

For long-running tasks or CI/CD, use git branches instead of /rewind:

```bash
# On claim: create branch
git checkout -b mentu/cmt_xxx

# During work: commit at logical points
git add -A && git commit -m "Add feature X"

# On submit: merge and cleanup
git checkout main
git merge --squash mentu/cmt_xxx
```

**When to use which:**

| Situation | Use |
|-----------|-----|
| Undo last few edits | `/rewind` |
| Bash broke something | `git revert` |
| Start over | `git reset --hard` |

See `skills/mentu-git-workflow/SKILL.md` for full workflow.

## Links

- [Mentu Documentation](https://mentu.ai/docs)
- [Protocol Specification](https://github.com/mentu-ai/mentu/blob/main/docs/Mentu-Spec-v0.md)
- [Report Issues](https://github.com/mentu-ai/mentu-plugin/issues)

## License

MIT

---

*Agents start warm, every action leaves evidence, validation scales with risk.*
