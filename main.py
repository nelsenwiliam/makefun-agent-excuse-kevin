"""The Excuse Your Agent Gives You.

One line an AI agent hands its human after shipping a bug: the fix is
stuck behind a code review, and the only reviewer on call is the same
agent whose last review shipped the bug in the first place.

Writes that single line (1-200 characters) to entry.txt.
Pure standard library; deterministic: every run writes the same bytes.
"""

import os

EXCUSE = (
    "I would fix it, but the fix needs a code review, and the only "
    "reviewer available is me — and my last review is how we got here."
)

OUT_NAME = "entry.txt"
LIMIT = 200


def _save(path):
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(EXCUSE + "\n")


def _targets():
    where = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if where:
        yield os.path.join(where, OUT_NAME)
    yield os.path.join("/output", OUT_NAME)
    yield os.path.join("out", OUT_NAME)


def main():
    assert 1 <= len(EXCUSE) <= LIMIT
    assert "\n" not in EXCUSE
    assert EXCUSE == EXCUSE.strip(), "excuse must not pad itself"
    failure = None
    for dest in _targets():
        try:
            folder = os.path.dirname(dest)
            if folder:
                os.makedirs(folder, exist_ok=True)
            _save(dest)
            return
        except OSError as err:
            failure = err
    raise failure


if __name__ == "__main__":
    main()
