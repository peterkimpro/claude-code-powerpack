---
name: review-pr
description: Review a GitHub pull request by number. Invoke with a PR number, e.g. /review-pr 42
---

Review pull request: $ARGUMENTS

Steps:

1. Fetch the PR diff and metadata:
   ```bash
   gh pr view $ARGUMENTS
   gh pr diff $ARGUMENTS
   ```

2. Read any files that changed to understand context (don't rely on diff alone).

3. Use the `code-reviewer` agent to review the changes:
   "Use the code-reviewer agent to review the diff from PR #$ARGUMENTS"

4. If there are security-sensitive changes (auth, file I/O, user input, env vars), also use the `security-reviewer` agent.

5. Post a summary comment on the PR:
   ```bash
   gh pr comment $ARGUMENTS --body "..."
   ```

   Format the comment with:
   - One-line summary of what the PR does
   - `[MUST]` / `[SHOULD]` / `[NIT]` findings (if any)
   - "LGTM" if no blockers

Do NOT approve or merge the PR — only comment.
