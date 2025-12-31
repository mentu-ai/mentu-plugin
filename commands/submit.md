---
description: Submit commitment for review with evidence
---

# Submit Commitment

Submit the specified commitment for review.

## Steps

1. Ensure work is complete
2. Capture final evidence if not already done:
   ```bash
   mentu capture "Completed: <summary>" --kind evidence
   ```

3. Submit for review:
   ```bash
   mentu submit $ARGUMENTS --summary "<what was done>" --include-files
   ```

The commitment enters `in_review` state awaiting approval.

User provided: $ARGUMENTS
