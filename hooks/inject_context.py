#!/usr/bin/env python3
"""
Injects current git branch and recent diff summary into every prompt.
Keeps Claude aware of what's changed without you having to say it.
"""
import json
import subprocess
import sys


def main():
    try:
        json.load(sys.stdin)
    except Exception:
        pass

    try:
        branch = subprocess.check_output(
            ["git", "branch", "--show-current"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        diff_stat = subprocess.check_output(
            ["git", "diff", "--stat", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()

        if branch:
            print(f"[Context] Branch: {branch}")
        if diff_stat:
            print(f"Recent changes:\n{diff_stat}")
    except Exception:
        pass  # Not a git repo or git not available — silently skip


if __name__ == "__main__":
    main()
