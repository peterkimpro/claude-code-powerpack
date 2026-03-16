#!/usr/bin/env python3
"""
Blocks Claude from writing to CI config or production infra files
without an explicit override. Prevents expensive accidental edits.

To customize: edit the PROTECTED list below.
Exit code 2 blocks the tool call; output is shown as the reason.
"""
import json
import sys


PROTECTED = [
    ".github/workflows/",
    "terraform/",
    "k8s/",
]


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool = data.get("tool_name", "")
    params = data.get("tool_input", {})

    if tool in ("Write", "Edit"):
        path = params.get("file_path", "")
        for protected in PROTECTED:
            if path.startswith(protected):
                print(
                    f"BLOCK: {path} is a protected path ({protected}). "
                    "Ask the user to confirm before editing CI/infra files."
                )
                sys.exit(2)


if __name__ == "__main__":
    main()
