# CLAUDE.md

This file is read by Claude Code at the start of every session. Keep it concise — every line costs tokens.
Run `/init` to auto-generate a starter version from your codebase, then refine.

<!--
WHAT TO INCLUDE vs. EXCLUDE

✅ Include:
- Bash commands Claude can't guess (non-standard build steps, env setup)
- Code style rules that differ from language defaults
- Testing instructions and preferred test runners
- Repo etiquette (branch naming, PR conventions)
- Architectural decisions specific to this project
- Developer environment quirks (required env vars, local setup gotchas)
- Common non-obvious behaviors or footguns

❌ Exclude:
- Anything Claude can figure out by reading the code
- Standard language conventions Claude already knows
- Detailed API docs (link to them instead)
- Information that changes frequently
- File-by-file descriptions of the codebase
- Self-evident practices like "write clean code"

If Claude keeps ignoring a rule, the file is too long — prune it.
If Claude asks questions answered here, the phrasing is ambiguous — rewrite it.
-->

## Project Overview

[One sentence: what this project does and who it's for.]

## Tech Stack

- **Language:**
- **Package manager:**
- **Framework:**
- **Testing:**
- **Linting:**

## Key Commands

```bash
# Install dependencies
# Build
# Test (prefer single test over full suite for speed)
# Lint
# Type check
```

## Rules

- [e.g., never use npm, only pnpm]
- [e.g., all exports must be named, no default exports]
- [e.g., no `any` types]

## Out of Scope

- [Things Claude should NOT do without explicit instruction]
- [e.g., do not push to remote, do not modify CI config]

<!--
You can import other files into this CLAUDE.md:
  See @README.md for project overview
  See @docs/architecture.md for system design
  See @~/.claude/my-global-instructions.md for personal overrides
-->
