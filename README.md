# Claude Code Powerpack

The most complete Claude Code starter kit — distilled from the leading open-source repos, Anthropic's own best practices docs, and community tools. Drop it into any project and hit the ground running: persistent memory, lifecycle hooks, agents, skills, context optimization, and reusable workflows all pre-configured.

Built and maintained by [@peterkimpro](https://github.com/peterkimpro).

## What's Included

```
.claude/
├── settings.json          # Permission allowlist + deny list + lifecycle hooks
├── agents/
│   ├── security-reviewer  # Scans code for vulnerabilities before commit
│   └── code-reviewer      # Quality/correctness review for PRs and diffs
└── skills/
    ├── commit/            # /commit — stage + write conventional commit
    ├── review-pr/         # /review-pr <number> — review a GitHub PR
    └── scaffold/          # /scaffold <name> — create module following existing patterns

CLAUDE.md                  # Project instructions template (Claude reads this every session)
cheatsheet.md              # Commands, shortcuts, prompting patterns at a glance
hooks/
├── inject_context.py      # UserPromptSubmit — injects git branch + diff into every prompt
├── pre_tool_use.py        # PreToolUse — blocks writes to protected paths (CI/infra)
├── track_reads.py         # PostToolUse — logs files Claude reads to ~/.claude-reads.log
└── README.md              # Lifecycle hook reference + customization guide
memory/
├── MEMORY.md              # Memory index (loaded every session)
└── README.md              # How the memory system works
docs/
└── adr/                   # Architecture Decision Records template
```

## Quick Setup

### 1. Clone this repo

```bash
git clone https://github.com/peterkimpro/claude-code-powerpack.git
cd my-project
```

### 2. Copy the Claude config into your project

```bash
cp -r claude-code-powerpack/.claude ./
cp -r claude-code-powerpack/hooks ./
cp claude-code-powerpack/CLAUDE.md ./
```

### 3. Fill in CLAUDE.md

Edit `CLAUDE.md` with your project's specifics:
- One-line project description
- Tech stack and package manager
- Key commands (build, test, lint)
- Any hard rules for Claude to follow

### 4. Set up memory

Copy the memory templates to Claude's memory directory for your project:

```bash
# Find your project's encoded path
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^-||')
MEMORY_DIR="$HOME/.claude/projects/$PROJECT_PATH/memory"
mkdir -p "$MEMORY_DIR"
cp claude-code-powerpack/memory/MEMORY.md "$MEMORY_DIR/"
```

### 5. Configure your permission allowlist

Edit `.claude/settings.json` to add your project's common commands:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run build)",
      "Bash(npm test)",
      "Bash(npm run lint)"
    ],
    "deny": [
      "Read(./package-lock.json)",
      "Read(./node_modules/**)",
      "Read(./.DS_Store)"
    ]
  }
}
```

**Allow:** Commands Claude runs repeatedly. Allowlisting removes the approval prompt and cuts iteration overhead significantly.

**Deny:** Files Claude should never read. `node_modules` and `package-lock.json` are pure token waste — Claude will crawl them if not blocked. Add any other large auto-generated files in your project.

## Key Concepts

### Give Claude a Way to Verify Its Work

The single highest-leverage thing you can do. Claude performs dramatically better when it can check itself — run tests, compare output, validate a build. Without verification criteria, Claude produces something that looks right but may not work, and you become the only feedback loop.

```
# Instead of:
"implement a function that validates email addresses"

# Do this:
"write validateEmail(). test cases: user@example.com → true,
invalid → false, user@.com → false. run the tests after implementing."
```

If you can't verify it, don't ship it.

### CLAUDE.md — Session Instructions

Claude reads `CLAUDE.md` at the start of every session. Run `/init` to auto-generate a starter from your codebase, then refine.

**What to include vs. exclude:**

| ✅ Include | ❌ Exclude |
|-----------|-----------|
| Bash commands Claude can't guess | Anything derivable from reading the code |
| Code style rules that differ from defaults | Standard language conventions |
| Testing instructions and preferred runners | Detailed API docs (link instead) |
| Repo etiquette (branch naming, PR conventions) | Information that changes frequently |
| Architectural decisions specific to this project | File-by-file codebase descriptions |
| Environment quirks and required env vars | Self-evident practices ("write clean code") |

If Claude keeps ignoring a rule, the file is too long — prune it or convert the rule to a hook. If Claude asks questions answered in CLAUDE.md, the phrasing is ambiguous — rewrite it.

You can import other files directly:
```markdown
See @README.md for project overview
See @docs/architecture.md for system design
See @~/.claude/my-global-instructions.md for personal overrides
```

CLAUDE.md files stack: `~/.claude/CLAUDE.md` (global) → project root → parent dirs → child dirs (loaded on demand).

### The 4-Step Workflow (Plan Mode)

For tasks that touch multiple files or where the approach is unclear:

1. **Explore** (Plan Mode) — read files, understand the system, no changes made
2. **Plan** (Plan Mode) — ask Claude for a full implementation plan; `Ctrl+G` opens it in your editor
3. **Implement** (Normal Mode) — code + verify against tests/output
4. **Commit** — commit with descriptive message, open PR

Toggle Plan Mode with `Shift+Tab`. Skip it for small, obvious changes — planning adds overhead.

### Permission Allowlist — Remove Friction

Every unapproved command stops Claude and waits for you. The allowlist in `.claude/settings.json` auto-approves specific commands. Add commands you trust; keep destructive operations (push, reset, drop) out of it.

Deny list blocks files Claude should never read — `node_modules`, lock files, and generated output are pure token waste.

### Hooks — Automatic Context Injection

Hooks in `.claude/settings.json` run shell commands at key lifecycle points — before a prompt is processed, before/after a tool call, when Claude stops. Unlike CLAUDE.md instructions (advisory), hooks are deterministic and guaranteed to run. Use them to:
- **Inject context automatically** — git branch, recent diff, env state — without saying it every session
- **Block dangerous operations** — prevent writes to CI/infra files without confirmation
- **Track behavior** — log which files Claude actually reads to tune your deny list

See `hooks/README.md` for example scripts and the full event reference.

### Agents — Specialized Subprocesses

Agents in `.claude/agents/` run in their own context window with their own tools. They're the primary way to keep your main context clean — delegate investigation and review work to agents so their file reads don't accumulate in your session.

Use agents for:
- Repeatable review tasks (security, code quality)
- Tasks that need a different model (Opus for deep reasoning, Haiku for speed)
- Any research/investigation that would otherwise pollute main context

### Skills — Slash Commands

Skills in `.claude/skills/` become `/skill-name` slash commands. They encode multi-step workflows so you don't re-explain them each session. Add `disable-model-invocation: true` to the frontmatter for skills with side effects that should only run when explicitly invoked.

### Memory — Persistent Context

Without memory, Claude starts from zero every session. The memory system at `memory/MEMORY.md` gives Claude a persistent understanding of your project, your preferences, and corrections you've given.

The highest-value memory type is **feedback** — corrections that prevent Claude from making the same mistake twice.

### Context Management

Context is the fundamental constraint. As it fills, performance degrades.

| Command | Use it when |
|---------|------------|
| `/clear` | Switching to an unrelated task |
| `/compact <focus>` | Context is getting full but you want to continue |
| `/rewind` or `Esc Esc` | Claude went off track — restore to a prior checkpoint |
| `/btw <question>` | Quick side question that shouldn't pollute history |
| `Esc` | Stop Claude mid-action and redirect |

Rule of thumb: if you've corrected Claude on the same issue twice, `/clear` and write a better initial prompt — don't keep patching a polluted context.

### Session Management

```bash
claude --continue    # Resume the most recent conversation
claude --resume      # Pick from recent conversations
```

Use `/rename <name>` to name sessions (`oauth-migration`, `perf-debugging`) so you can find them across days. Treat sessions like branches — different workstreams get separate persistent contexts.

### Non-Interactive Mode (CI / Scripts)

```bash
claude -p "prompt"                                  # One-off, plain text output
claude -p "prompt" --output-format json             # Structured JSON
claude -p "prompt" --output-format stream-json      # Streaming JSON
claude -p "prompt" --allowedTools "Edit,Bash(git commit *)"  # Scope permissions
```

Fan-out pattern for large migrations:
```bash
for file in $(cat files.txt); do
  claude -p "migrate $file from React to Vue. return OK or FAIL." \
    --allowedTools "Edit,Bash(git commit *)"
done
```

Test on 2–3 files first, then run at scale.

### Parallel Sessions (Writer/Reviewer)

Fresh context makes better reviewers — Claude won't be biased toward code it just wrote.

| Session A (Writer) | Session B (Reviewer) |
|---|---|
| `implement rate limiter for API endpoints` | |
| | `review @src/middleware/rateLimiter.ts — look for edge cases, race conditions, and consistency with existing middleware` |
| `here's the review: [paste]. address these issues.` | |

## Common Failure Patterns

| Pattern | Fix |
|---------|-----|
| **Kitchen sink session** — jumped between tasks, context is polluted | `/clear` between unrelated tasks |
| **Correction loop** — corrected the same issue 2+ times | `/clear` and rewrite the initial prompt with what you learned |
| **Bloated CLAUDE.md** — Claude ignores rules buried in noise | Ruthlessly prune; convert rules to hooks for guaranteed enforcement |
| **Trust gap** — implementation looks right but has edge cases | Always provide verification (tests, scripts, screenshots) |
| **Infinite exploration** — Claude read 200 files, context is full | Scope investigations narrowly or delegate to a subagent |

## Customizing

### Add a new skill

Create `.claude/skills/<skill-name>/SKILL.md`:

```markdown
---
name: my-skill
description: What this skill does. Claude uses this to decide when to invoke it.
---

Do the thing: $ARGUMENTS

Steps:
1. ...
2. ...
```

Then invoke it in a session with `/my-skill`.

### Add a new agent

Create `.claude/agents/<agent-name>.md`:

```markdown
---
name: my-agent
description: When Claude should use this agent (be specific).
tools: Read, Grep, Glob, Bash
model: claude-sonnet-4-6
---

You are a [role]. Your job is to [task].

[Instructions...]
```

### Add MCP servers

MCP (Model Context Protocol) servers extend Claude with external tools — file systems, databases, APIs, browsers. Configure them in Claude's global settings at `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allow"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "..." }
    }
  }
}
```

See [MCP server directory](https://github.com/modelcontextprotocol/servers) for available servers.

## Community Skills

The `skills` CLI is a third-party package manager for installing community-published SKILL.md files directly into your `.claude/skills/` directory.

```bash
npx skills find                          # Interactive search of published skills
npx skills add <owner/repo/skills> -y   # Install all skills from a repo
npx skills add <owner/repo@skill> -y    # Install a specific skill
npx skills list                          # List installed skills
npx skills remove <skill>               # Remove a skill
```

Skills install into `.claude/skills/` and become immediately available as `/skill-name` commands in Claude Code.

### Notable Skill Packages

| Package | What it adds | Install |
|---------|-------------|---------|
| [google/adk-docs](https://github.com/google/adk-docs/tree/main/skills) | 6 skills for Google ADK agent development — API cheatsheet, dev/deploy/eval guides, scaffolding. Eliminates hallucinated ADK methods. | `npx skills add google/adk-docs/skills -y` |

> **ADK skills** are only relevant if you're building with Google's Agent Development Kit (Python/TS/Go/Java). They give Claude accurate knowledge of ADK APIs, deployment to Agent Engine + Cloud Run, evaluation methodology, and observability setup.

To publish your own skills for the community: create a `skills/` directory in any public GitHub repo with `SKILL.md` files following the standard format. Anyone can install them with `npx skills add <your-org/your-repo/skills>`.

## Plugins

Claude Code supports plugins installable via `/plugin marketplace add <author/repo>`.

| Plugin | What it does | Install |
|--------|-------------|---------|
| [claude-mem](https://github.com/thedotmack/claude-mem) | Persistent memory compression — SQLite + vector DB, auto-capture via hooks, ~10x token savings, web viewer | `/plugin marketplace add thedotmack/claude-mem` |

See `memory/README.md` for when to use `claude-mem` vs. the built-in memory system.

## Advanced Context Optimization

For large or complex codebases where token usage becomes a bottleneck:

**[CC-RLM](https://github.com/michaewahl/CC-RLM)** — A proxy layer that sits between Claude Code and a local LLM (Ollama/vLLM). Instead of dumping full files into context, it maintains a live structural model of the repo — import graphs, AST symbol slices, git diffs — and assembles a targeted context pack under 8K tokens per request.

- **82% token reduction** vs. naive full-repo injection
- **88% recall** — the right files actually make it in
- **<200ms** context build latency
- Self-improving: files Claude actually uses get higher relevance scores (persisted in SQLite)

Requires Docker + Python 3.13 + Ollama or vLLM. Not a drop-in — it's infrastructure. The hooks pattern in `hooks/README.md` captures the same idea at a lighter weight.

The key insight from CC-RLM: **code relevance is structural, not semantic.** Follow imports. Check the call graph. Look at the diff. Don't vector-search.

## Resources

- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [MCP server directory](https://github.com/modelcontextprotocol/servers)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Contributing

PRs welcome. The goal is a minimal, generic foundation — not a framework. Keep additions focused on reducing iteration overhead, not adding features.
