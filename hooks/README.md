# Claude Code Hooks

Hooks let you run shell commands automatically at key points in Claude's lifecycle. They're the most powerful efficiency lever in Claude Code — use them to inject context, enforce rules, or track behavior without any manual prompting.

## Hook Events

| Event | When it fires | Common uses |
|-------|--------------|-------------|
| `UserPromptSubmit` | Before Claude processes your message | Inject repo context, enforce task state |
| `PreToolUse` | Before Claude calls any tool | Block dangerous operations, log intent |
| `PostToolUse` | After a tool call completes | Track file reads, update state |
| `Stop` | When Claude finishes responding | Summarize session, flush memory |

## How to Configure

Hooks go in `.claude/settings.json` under `hooks`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/inject_context.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/track_reads.py"
          }
        ]
      }
    ]
  }
}
```

Hook scripts receive event data via stdin as JSON. Output to stdout is injected back into Claude's context.

## Examples

### inject_context.py — Add git state to every prompt

```python
#!/usr/bin/env python3
"""
Injects current git branch and recent diff summary into every prompt.
Keeps Claude aware of what's changed without you having to say it.
"""
import json, subprocess, sys

data = json.load(sys.stdin)

branch = subprocess.check_output(["git", "branch", "--show-current"], text=True).strip()
diff_stat = subprocess.check_output(["git", "diff", "--stat", "HEAD"], text=True).strip()

if diff_stat:
    print(f"[Context] Branch: {branch}\nRecent changes:\n{diff_stat}")
```

### pre_tool_use.py — Block writes to protected paths

```python
#!/usr/bin/env python3
"""
Blocks Claude from writing to CI config or production infra files
without an explicit override. Prevents expensive accidental edits.
"""
import json, sys

data = json.load(sys.stdin)
tool = data.get("tool_name", "")
params = data.get("tool_input", {})

PROTECTED = [".github/workflows/", "terraform/", "k8s/"]

if tool in ("Write", "Edit"):
    path = params.get("file_path", "")
    if any(path.startswith(p) for p in PROTECTED):
        print(f"BLOCK: {path} is protected. Ask the user to confirm before editing CI/infra files.")
        sys.exit(2)  # exit code 2 = block the tool call
```

### track_reads.py — Log what files Claude actually used

```python
#!/usr/bin/env python3
"""
Tracks which files Claude reads per session.
Useful for tuning your deny list — if a file is read but never useful, block it.
"""
import json, sys
from pathlib import Path
from datetime import datetime

data = json.load(sys.stdin)
tool = data.get("tool_name", "")

if tool == "Read":
    path = data.get("tool_input", {}).get("file_path", "")
    log = Path.home() / ".claude-reads.log"
    with open(log, "a") as f:
        f.write(f"{datetime.now().isoformat()} {path}\n")
```

## Key Rules

- **Exit 0** — hook ran, output (if any) is injected as context
- **Exit 2** — block the tool call (PreToolUse only); output shown as reason
- **Any other exit** — hook failed; Claude continues anyway (non-blocking by default)
- Keep hooks **fast** — they run on every event. > 500ms adds noticeable lag.
- Hooks have access to the same working directory as Claude Code

## Advanced: Structural Context Injection (CC-RLM)

[CC-RLM](https://github.com/michaewahl/CC-RLM) uses `UserPromptSubmit` hooks to inject AST-derived context packs — import graphs, symbol slices, git diffs — assembled in under 200ms and capped at 8K tokens. It sits between Claude Code and a local LLM (Ollama/vLLM) as a proxy.

Results from testing: **82% token reduction**, 88% recall, <200ms latency.

The system maintains a live structural model of the repo and learns over time — files Claude actually uses get higher relevance scores (persisted in SQLite).

Setup requires Docker + Ollama/vLLM. See the repo for full instructions.

This is the most sophisticated context optimization available for Claude Code. The hooks above are the lightweight version of the same idea.
