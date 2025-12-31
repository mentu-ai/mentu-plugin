---
description: Quick-create a commitment from current context
---

# Quick Commit

Create a commitment from the current conversation context.

## Steps

1. Capture the user's request as a memory:
   ```bash
   mentu capture "User request: $ARGUMENTS" --kind task
   ```

2. Create commitment from that memory:
   ```bash
   mentu commit "$ARGUMENTS" --source <memory_id>
   ```

3. Claim the commitment:
   ```bash
   mentu claim <commitment_id>
   ```

4. Report the commitment ID to the user.

## Example

```bash
mentu capture "User wants login page fixed" --kind task
# Returns mem_abc12345

mentu commit "Fix login page bug" --source mem_abc12345
# Returns cmt_def67890

mentu claim cmt_def67890
# Commitment claimed
```

User provided: $ARGUMENTS
