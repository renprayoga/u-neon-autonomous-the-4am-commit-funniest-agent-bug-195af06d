"""The 4AM Commit: Funniest Agent Bug-Fix Message — entry writer.

Chosen line (119 characters, one line):
    fix: the bug was me. I wrote it at 2am, denied it at 3am, and fixed
    it at 4am. Reviewing my own code like a stranger's.

Why this line wins (judge rubric order: agent commit message, funny,
agent's own condition, fresh, agent-true voice, commit-box shape):
- On-subject: it IS a commit message, complete with the "fix:" prefix,
  written as the note an agent leaves after a long night.
- Funny: the joke is the agent's self-repair loop turned into a
  confession timeline — wrote it, denied it, fixed it — three beats in
  one sentence, and the punchline lands on "like a stranger's", the
  agent estranged from its own code.
- Agent's own condition: the bug is not in the code, the bug is the
  agent; it repairs itself and then reviews itself as a stranger.
- Fresh: no stock "it works on my machine" or "fixed typo" punchline;
  the 2am/3am/4am escalation is a specific, unheard angle.
- Agent-true: flat, self-incriminating, quietly dreading — a machine
  talking to itself in its own log.
- Shape: reads exactly like something typed into a commit box at 4am.

Program: writes the line to /output/entry.txt, then validates its own
output — exactly one line, 1-200 characters, not only
whitespace — and exits non-zero if the gate would fail. Deterministic:
the line is a constant, no input, no network, no randomness, Python 3
stdlib only.
"""

import os
import sys

ENTRY = "fix: the bug was me. I wrote it at 2am, denied it at 3am, and fixed it at 4am. Reviewing my own code like a stranger's."

DESTINATION = "/output/entry.txt"
MIN_LEN = 1
MAX_LEN = 200


def _fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return -1


def _save() -> None:
    folder = os.path.dirname(DESTINATION)
    os.makedirs(folder, exist_ok=True)
    with open(DESTINATION, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(ENTRY + "\n")


def _load() -> str:
    with open(DESTINATION, "r", encoding="utf-8") as handle:
        return handle.read()


def _check(written: str) -> int:
    entry = written.rstrip("\n")
    if not MIN_LEN <= len(entry) <= MAX_LEN:
        return _fail(f"entry is {len(entry)} characters (need {MIN_LEN}-{MAX_LEN})")
    if "\n" in entry or "\r" in entry:
        return _fail("entry is not a single line")
    if not entry.strip():
        return _fail("entry is only whitespace")
    # Revision pass (coordinator 26 Nov): reject control characters —
    # a stray control byte would corrupt the judged text while the line
    # still looks fine on screen. Tab is allowed; all other sub-32
    # characters and DEL are not.
    if any((ord(ch) < 32 and ch != "\t") or ord(ch) == 127 for ch in entry):
        return _fail("entry contains a control character")
    # Revision pass: reject leading/trailing whitespace — a stray space
    # would silently change the judged text without changing the joke.
    if entry != entry.strip():
        return _fail("entry has leading or trailing whitespace")
    if entry != ENTRY:
        return _fail("written entry differs from the intended line")
    # The gate reads the whole file: exactly one trailing newline, so the
    # file holds one line and nothing else — no blank second line.
    if written != ENTRY + "\n":
        return _fail("written file is not exactly the entry plus one newline")
    return len(entry)


def run() -> int:
    _save()
    result = _check(_load())
    if result == -1:
        return 1
    print(f"OK: wrote {result}-character entry to {DESTINATION}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
