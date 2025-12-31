---
name: mentu-git-workflow
description: Git-backed recovery with diff evidence trail. Use in git repos for persistent, structured recovery that complements /rewind.
---

# Mentu Git Workflow

Use git branches for recovery and git diffs for evidence. Complements Claude Code checkpoints.

## When To Use This Skill

- Working in a git repository
- Long-running or CI/CD tasks
- Need to recover from Bash/npm/git changes (not tracked by /rewind)
- Want persistent history across sessions

## Two-Layer Recovery Model

| Layer | Mechanism | Scope | Use For |
|-------|-----------|-------|---------|
| **Checkpoints** | /rewind | Edit/Write only | Quick undo, last few steps |
| **Git** | reset/revert | ALL changes | Start over, undo feature |

## Workflow

### On Claim

```bash
# Create work branch (recovery point)
git checkout -b mentu/cmt_<id>

# Capture baseline
mentu capture "Branch: mentu/cmt_<id>, Base: $(git rev-parse --short HEAD)" \
  --kind baseline
```

### During Work

Commit at logical boundaries (not every file):

```bash
# After completing a logical unit
git add -A
git commit -m "<what this change does>"

# Optional: capture diff as evidence
mentu capture "$(git diff HEAD~1 --stat)" --kind work-step
```

Good commit points:
- "Add authentication endpoint"
- "Fix email validation"
- "Update tests for auth"

### On Submit

```bash
# Full evidence
COMMITS=$(git log main..HEAD --oneline)
DIFF=$(git diff main...HEAD --stat)

mentu submit cmt_<id> \
  --summary "Commits: $COMMITS" \
  --include-files
```

### On Approve

```bash
# Merge and cleanup
git checkout main
git merge --squash mentu/cmt_<id>
git commit -m "cmt_<id>: <description>"
git branch -d mentu/cmt_<id>
```

### On Reject

Choose based on scope of fix needed:

```bash
# Small fix (still in session)
/rewind  # Use checkpoints

# Small fix (new session)
# Just fix and amend
git add -A && git commit --amend

# One commit was bad
git revert <hash>

# Start over
git checkout main
git branch -D mentu/cmt_<id>
git checkout -b mentu/cmt_<id>
```

## Recovery Decision Tree

```
PROBLEM OCCURS
      |
      +-- Last few Edit/Write changes?
      |         +-- /rewind (fast)
      |
      +-- Bash/npm/git broke something?
      |         +-- git revert or reset (git tracked it)
      |
      +-- One specific commit bad?
      |         +-- git revert <hash>
      |
      +-- Whole approach wrong?
                +-- git reset --hard main
```

## Coverage Matrix

| Change Type | /rewind? | git? |
|-------------|----------|------|
| Edit tool | Yes | Yes |
| Write tool | Yes | Yes |
| Bash rm/mv/cp | No | Yes |
| npm install | No | Yes |
| git commands | No | Yes |

## CI/CD Usage

### GitHub Actions

```yaml
- uses: anthropics/claude-code-action@beta
  with:
    prompt: |
      Follow mentu-git-workflow skill.
      Create branch mentu/cmt_<id>.
      Commit at logical boundaries.
      Submit when complete.
```

### GitLab CI/CD

```yaml
script:
  - claude -p "Follow mentu-git-workflow skill..." \
      --permission-mode acceptEdits
```

## Constraints

- **No interactive commands**: Use `git revert`, not `git rebase -i`
- **No force push**: Standard branch protection applies
- **Branch naming**: Always `mentu/cmt_<id>`

## Key Insight

**Checkpoints = speed. Git = structure. Mentu = proof.**

Use /rewind for quick undo of recent Edit/Write.
Use git for structured recovery of everything.
Use Mentu to prove what happened and why.
