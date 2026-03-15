# Claude Code Quickstart

A drop-in file structure to get Claude Code running efficiently from day one — fewer prompt iterations, persistent memory, and reusable workflows baked in.

## What's Included

```
.claude/
├── settings.json          # Bash permission allowlist (auto-approve common commands)
├── agents/
│   ├── security-reviewer  # Scans code for vulnerabilities before commit
│   └── code-reviewer      # Quality/correctness review for PRs and diffs
└── skills/
    ├── commit/            # /commit — stage + write conventional commit
    ├── review-pr/         # /review-pr <number> — review a GitHub PR
    └── scaffold/          # /scaffold <name> — create module following existing patterns

CLAUDE.md                  # Project instructions template (Claude reads this every session)
memory/
├── MEMORY.md              # Memory index (loaded every session)
└── README.md              # How the memory system works
```

## Quick Setup

### 1. Clone this repo

```bash
git clone https://github.com/peterkim676/claude-code-quickstart.git
cd my-project
```

### 2. Copy the Claude config into your project

```bash
cp -r claude-code-quickstart/.claude ./
cp claude-code-quickstart/CLAUDE.md ./
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
cp claude-code-quickstart/memory/MEMORY.md "$MEMORY_DIR/"
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
    ]
  }
}
```

Add whatever commands Claude runs repeatedly. Allowlisting them removes the approval prompt and cuts iteration overhead significantly.

## Key Concepts

### CLAUDE.md — Session Instructions

Claude reads `CLAUDE.md` at the start of every session. Keep it under ~100 lines:
- Long CLAUDE.md = more tokens consumed before Claude writes a single line of code
- Be explicit about what Claude should NOT do (prevents expensive mistakes)
- Tech stack + key commands are the highest-value content

### Permission Allowlist — Remove Friction

Every unapproved command stops Claude and waits for you. The allowlist in `.claude/settings.json` auto-approves specific commands. Add commands you trust; keep destructive operations (push, reset, drop) out of it.

### Agents — Specialized Subprocesses

Agents in `.claude/agents/` are invoked by Claude automatically based on the task. They run with a focused system prompt and can be assigned specific tools and models. Use agents for:
- Repeatable review tasks (security, code quality)
- Tasks that need a different model (Opus for deep reasoning, Haiku for speed)
- Keeping the main context window clean

### Skills — Slash Commands

Skills in `.claude/skills/` become `/skill-name` slash commands. They encode multi-step workflows so you don't re-explain them each session. Use skills for:
- Repeated workflows (commit, deploy, scaffold)
- Anything with more than 3 steps
- Workflows that involve multiple agents

### Memory — Persistent Context

Without memory, Claude starts from zero every session. The memory system at `memory/MEMORY.md` gives Claude a persistent understanding of your project, your preferences, and corrections you've given.

The highest-value memory type is **feedback** — corrections that prevent Claude from making the same mistake twice.

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

## Resources

- [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code)
- [MCP server directory](https://github.com/modelcontextprotocol/servers)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Contributing

PRs welcome. The goal is a minimal, generic foundation — not a framework. Keep additions focused on reducing iteration overhead, not adding features.
