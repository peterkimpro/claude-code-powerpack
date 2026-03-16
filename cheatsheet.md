# Claude Code Cheatsheet

Quick reference for commands, shortcuts, and patterns.

## Session Commands

| Command | What it does |
|---------|-------------|
| `/clear` | Reset context window. Use between unrelated tasks. |
| `/compact` | Compress conversation history to free context. |
| `/compact <instructions>` | Compact with focus, e.g. `/compact focus on the API changes` |
| `/rewind` | Open checkpoint menu — restore conversation, code, or both to any prior state. |
| `Esc` | Stop Claude mid-action. Context preserved, you can redirect. |
| `Esc Esc` | Open rewind/checkpoint menu. |
| `/btw <question>` | Ask a side question. Answer appears in a dismissible overlay and **never enters conversation history**. |
| `/rename <name>` | Name the current session (e.g., `oauth-migration`). Makes it findable later. |
| `/init` | Auto-generate a starter CLAUDE.md from your codebase structure. |
| `/hooks` | Browse configured lifecycle hooks. |
| `/permissions` | View and edit the permission allowlist interactively. |
| `/sandbox` | Enable OS-level isolation. |

## CLI Flags

```bash
claude --continue          # Resume the most recent conversation
claude --resume            # Pick from recent conversations
claude -p "prompt"         # Non-interactive mode (CI, scripts)
claude -p "prompt" --output-format json          # Structured JSON output
claude -p "prompt" --output-format stream-json   # Streaming JSON
claude -p "prompt" --allowedTools "Edit,Bash(git commit *)"  # Scope permissions
claude -p "prompt" --verbose  # Debug output
```

## The 4-Step Workflow (Plan Mode)

For any task touching multiple files or where you're unsure of the approach:

```
1. EXPLORE  (Plan Mode)   → read files, understand the system, no changes
2. PLAN     (Plan Mode)   → ask Claude to create an implementation plan
                            Ctrl+G to open the plan in your editor
3. IMPLEMENT (Normal)     → code + verify (run tests, check output)
4. COMMIT   (Normal)      → commit with descriptive message, open PR
```

Enter Plan Mode: `Shift+Tab` (toggle). Skip planning for small, obvious changes.

## Context Management

- **`/clear`** between unrelated tasks — don't let old context pollute new work
- **`/btw`** for quick questions that don't need to stay in history
- **Use subagents** for investigation — they read files in a separate context window, keeping yours clean
- **Scope prompts** — "investigate auth in src/auth/" beats "investigate auth"
- If Claude keeps making the same mistake: `/clear` and write a better initial prompt rather than keep correcting

## Prompting Patterns

**Verification** — always give Claude a way to check its own work:
```
implement validateEmail(). test cases: user@example.com → true,
invalid → false. run the tests after implementing.
```

**Point to patterns** — reference existing code:
```
look at HotDogWidget.php for the pattern, then implement a CalendarWidget
following the same structure.
```

**Scope the bug** — symptom + location + success criteria:
```
login fails after session timeout. check src/auth/ token refresh.
write a failing test that reproduces it, then fix it.
```

**Interview mode** — for large features, let Claude ask the questions:
```
I want to build [X]. Interview me using the AskUserQuestion tool.
Ask about edge cases, tradeoffs, and implementation details.
When done, write a spec to SPEC.md.
```

## Parallel Sessions (Writer/Reviewer)

| Session A (Writer) | Session B (Reviewer) |
|---|---|
| `implement rate limiter for API endpoints` | |
| | `review @src/middleware/rateLimiter.ts — look for edge cases, race conditions, consistency with existing middleware` |
| `here's review feedback: [paste]. address these issues.` | |

Fresh context makes better reviewers — Claude won't be biased toward code it just wrote.

## Fan-out for Large Migrations

```bash
# Generate file list, then loop
for file in $(cat files.txt); do
  claude -p "migrate $file from React to Vue. return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Test on 2-3 files first, then run at scale.

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Kitchen sink session | Jumped between tasks, context is a mess | `/clear` between unrelated tasks |
| Correction loop | Corrected same issue 2+ times | `/clear` and write a better initial prompt |
| Bloated CLAUDE.md | Claude ignores rules | Ruthlessly prune — convert rules to hooks if needed |
| Trust gap | Implementation looks right but has edge cases | Always provide verification (tests, scripts, screenshots) |
| Infinite exploration | Claude read 200 files, context is full | Scope the investigation or use subagents |
