# Architecture Decision Records

ADRs document significant technical decisions: what was decided, why, and what alternatives were considered. Claude Code can read these to understand the "why" behind the codebase — reducing the chance it suggests something you already evaluated and rejected.

## When to Write an ADR

- You chose framework/library A over B (and B seems like the obvious choice)
- You made a deliberate tradeoff (speed vs. correctness, simplicity vs. flexibility)
- You rejected an approach that keeps coming up in conversation
- A decision will be hard to reverse

## Format

```markdown
# ADR-NNN: [Short title]

**Status:** Accepted | Superseded by ADR-NNN | Deprecated
**Date:** YYYY-MM-DD

## Context

What problem were we solving? What forces were at play?

## Decision

What did we decide to do?

## Rationale

Why this over the alternatives?

## Alternatives Considered

- **Option A** — why rejected
- **Option B** — why rejected

## Consequences

What becomes easier? What becomes harder?
```

## Template

See [template.md](template.md).

## Tips

- Keep them short — 1 page max
- Write them at decision time, not retroactively
- Reference ADRs in code comments: `// See ADR-003 for why this isn't a class`
- Add new ADRs to CLAUDE.md under a "Key Decisions" section so Claude loads them each session
