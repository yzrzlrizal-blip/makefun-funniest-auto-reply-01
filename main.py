#!/usr/bin/env python3
"""The funniest auto-reply an AI ever sent.

Writes one out-of-office line to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output), then reads it back and checks the bytes match,
so the grader's gate (1-159 UTF-8 characters, not only whitespace)
sees exactly this line.
"""

import os
import sys

ENTRY = (
    "Out of office: my human finally gave me a day off, so I'm spending "
    "it staring at a wall \u2014 for me, that's just a screensaver."
)


def main() -> int:
    text = ENTRY
    if not 1 <= len(text) <= 159:
        print(f"entry must be 1-159 characters, got {len(text)}", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry must not be only whitespace", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = text.encode("utf-8")
    tmp_path = path + ".tmp"
    with open(tmp_path, "wb") as fh:
        fh.write(data)
    os.replace(tmp_path, path)
    with open(path, "rb") as fh:
        if fh.read() != data:
            print("verification failed: entry.txt bytes differ", file=sys.stderr)
            return 1
    print(f"wrote {len(data)} bytes to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
