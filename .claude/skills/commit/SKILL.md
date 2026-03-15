---
name: commit
description: Stage and commit all changes with a well-formed conventional commit message.
---

Create a git commit for the current changes.

Steps:

1. Run `git status` and `git diff` to review what changed.

2. Stage relevant files. Prefer staging specific files over `git add -A`. Never stage:
   - `.env` or any secrets file
   - Large binaries or generated files that shouldn't be tracked

3. Write a commit message following Conventional Commits:
   - Format: `<type>(<scope>): <short summary>`
   - Types: `feat`, `fix`, `chore`, `docs`, `refactor`, `test`, `ci`
   - Summary: present tense, under 72 chars, no period at end
   - Add a body if the change needs explanation (what and why, not how)

4. Commit using:
   ```bash
   git commit -m "$(cat <<'EOF'
   <message here>

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
   EOF
   )"
   ```

5. Run `git status` to confirm the commit succeeded.

Do NOT push unless the user explicitly asks.
