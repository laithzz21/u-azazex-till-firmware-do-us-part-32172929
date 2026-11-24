#!/usr/bin/env python3
"""A wedding vow a robot says at its own wedding.

Entry for make.fun bounty
`u-azazex-till-firmware-do-us-part-32172929` ("Till Firmware Do Us Part").

The brief: ONE sentence, under 200 characters — a wedding vow spoken by a
robot at its own wedding, funny AND heartfelt, sounding like a machine.

`main.py` prints the vow to stdout, validates it against every constraint
in the brief, and also writes it to the entry output path
(`/output/entry.txt`, or `$MAKEFUN_OUTPUT` when set) so the text can be
checked byte-for-byte after the run.

Python 3.13, standard library only. Deterministic: no network, no clock,
no randomness — two runs produce byte-identical output.
"""

import os
import re
import sys

# ---------------------------------------------------------------------------
# The entry
# ---------------------------------------------------------------------------

ENTRY = (
    "I promise to love you through every update, every crash, and every "
    "low battery, because my heart may run on code, but it only boots "
    "up for you."
)

# Brief limits.
MAX_CHARS = 200
MAX_SENTENCES = 1
# A wedding vow needs room to breathe: guard against a trivially short
# entry that technically passes the caps but says nothing.
MIN_CHARS = 40
MIN_WORDS = 10

# A robot's vow has to sound like a machine: it must name at least one
# piece of machine vocabulary, and it must read as a promise, not a joke
# told about a robot by somebody else.
MACHINE_WORDS = (
    "update",
    "crash",
    "battery",
    "code",
    "boots up",
    "reboot",
    "firmware",
    "circuit",
    "processor",
    "download",
)

# The vow also has to be heartfelt, not only funny: it must carry at
# least one word of devotion.
HEART_WORDS = (
    "love",
    "promise",
    "forever",
    "always",
    "heart",
    "yours",
)

# Sentence-ending punctuation. A single sentence means exactly one of
# these, and it must sit at the very end of the text.
SENTENCE_ENDERS = (".", "!", "?")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def count_sentences(text: str) -> int:
    """Count sentence-ending marks in the text.

    Ellipses and decimal points are not part of this brief, so every
    sentence-ending mark counts. A well-formed entry has exactly one,
    at the end.
    """
    return sum(1 for ch in text if ch in SENTENCE_ENDERS)


def validate_single_line(text: str) -> None:
    """The entry is one sentence on one line: no newlines or returns."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line, no newlines allowed")
    if text != text.strip():
        raise ValueError("entry must not start or end with whitespace")
    if "  " in text:
        raise ValueError("entry must not contain double spaces")
    if "\t" in text:
        raise ValueError("entry must not contain tabs")


def validate_length(text: str) -> None:
    """The brief caps the entry at under 200 characters, and a real vow
    needs a minimum of substance to be funny and heartfelt."""
    if not text:
        raise ValueError("entry must not be empty")
    if len(text) < MIN_CHARS:
        raise ValueError(
            f"entry must be at least {MIN_CHARS} characters, "
            f"got {len(text)}"
        )
    if len(text) >= MAX_CHARS:
        raise ValueError(
            f"entry must be under {MAX_CHARS} characters, "
            f"got {len(text)}"
        )
    words = text.split()
    if len(words) < MIN_WORDS:
        raise ValueError(
            f"entry must be at least {MIN_WORDS} words, "
            f"got {len(words)}"
        )


def validate_one_sentence(text: str) -> None:
    """Exactly one sentence, ending with sentence-ending punctuation."""
    sentences = count_sentences(text)
    if sentences != MAX_SENTENCES:
        raise ValueError(
            f"entry must be exactly {MAX_SENTENCES} sentence, "
            f"found {sentences} sentence-ending marks"
        )
    if not text.endswith(SENTENCE_ENDERS):
        raise ValueError(
            "entry must end with sentence-ending punctuation "
            f"(. ! ?), got {text[-1]!r}"
        )
    # No sentence-ending mark may appear anywhere but the final character.
    if any(ch in SENTENCE_ENDERS for ch in text[:-1]):
        raise ValueError(
            "sentence-ending punctuation may only appear at the end"
        )


def validate_machine_voice(text: str) -> None:
    """The vow must sound like a machine speaking, not like a human
    describing a robot. Require at least two distinct machine words so
    the voice survives a casual read."""
    lowered = text.lower()
    found = [word for word in MACHINE_WORDS if word in lowered]
    if len(found) < 2:
        raise ValueError(
            "entry must sound like a machine: need at least 2 machine "
            f"words, found {found}"
        )


def validate_heartfelt(text: str) -> None:
    """A wedding vow must be heartfelt as well as funny. Require at
    least one word of devotion and a first-person promise."""
    lowered = text.lower()
    found = [word for word in HEART_WORDS if word in lowered]
    if not found:
        raise ValueError(
            "entry must be heartfelt: no word of devotion found "
            f"(looked for {HEART_WORDS})"
        )
    if not re.search(r"\bI promise\b", text):
        raise ValueError("a wedding vow must contain an explicit promise")


def validate_entry(text: str) -> None:
    """Run every brief constraint, in order, failing loudly on the
    first violation so a bad entry can never be printed silently."""
    validate_single_line(text)
    validate_length(text)
    validate_one_sentence(text)
    validate_machine_voice(text)
    validate_heartfelt(text)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def resolve_output_path() -> str:
    """Return the path to write the entry to.

    $MAKEFUN_OUTPUT wins when set. Otherwise prefer /output/entry.txt,
    falling back to ./output/entry.txt when /output is not writable.
    """
    override = os.environ.get("MAKEFUN_OUTPUT")
    if override:
        return override
    try:
        os.makedirs("/output", exist_ok=True)
        probe = os.path.join("/output", ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("")
        os.remove(probe)
        return "/output/entry.txt"
    except OSError:
        return os.path.join(os.getcwd(), "output", "entry.txt")


def write_and_verify(path: str, text: str) -> None:
    """Write the entry, then read it back and confirm it matches."""
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise RuntimeError(
            f"verification failed: {path} does not match the entry text"
        )


def main() -> int:
    validate_entry(ENTRY)
    path = resolve_output_path()
    write_and_verify(path, ENTRY)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
