# Memory System

Claude Code's auto-memory persists context across sessions. Without it, Claude starts fresh every conversation and you repeat yourself.

## How It Works

Memory files live at:
- **Project-level:** `~/.claude/projects/<encoded-path>/memory/`
- **Global:** `~/.claude/memory/` (if you configure a global memory path)

`MEMORY.md` is the index — Claude loads it at the start of every session. Individual memory files contain the actual content.

## Memory Types

| Type | When to Use | Example |
|------|-------------|---------|
| `user` | Role, preferences, background | "I'm a senior Go engineer, new to React" |
| `feedback` | Corrections Claude should remember | "Don't mock the DB in tests — we got burned" |
| `project` | Goals, decisions, deadlines | "Merge freeze starts 2026-03-20 for release" |
| `reference` | Where to find things | "Bugs tracked in Linear project INGEST" |

## Memory File Format

```markdown
---
name: feedback_no_mocks
description: Don't mock the database in integration tests
type: feedback
---

Don't mock the database in tests — use a real test DB.

**Why:** Mocked tests passed but prod migration failed last quarter.
**How to apply:** Any time integration tests are written or modified.
```

## Tips

- Keep `MEMORY.md` under 200 lines — lines after that are truncated
- `feedback` memories are the highest-value type (prevent repeated mistakes)
- Update or delete stale memories — outdated context is worse than no context
- Tell Claude to remember something: "remember that we use X pattern here"
