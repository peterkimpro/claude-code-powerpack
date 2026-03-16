#!/usr/bin/env python3
"""
Tracks which files Claude reads per session to ~/.claude-reads.log.
Useful for tuning your deny list — if a file is read but never useful, block it.
"""
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")

    if tool == "Read":
        path = data.get("tool_input", {}).get("file_path", "")
        if path:
            log = Path.home() / ".claude-reads.log"
            try:
                with open(log, "a") as f:
                    f.write(f"{datetime.now().isoformat()} {path}\n")
            except Exception:
                pass  # Non-fatal — never block Claude over a logging failure


if __name__ == "__main__":
    main()
