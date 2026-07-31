#!/usr/bin/env python3
"""Verify that English and German templates use the same numbered structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path

__author__ = "Dr. Awanish Pratap Singh"

HEADING_PATTERN = re.compile(
    r"\\DFG(?:Stacked)?(?:DeepSubsubsection|Subsubsection|Subsection|Section)"
    r"\{([^}]+)\}\{"
)


def heading_numbers(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return HEADING_PATTERN.findall(text)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: check_language_parity.py ENGLISH.tex GERMAN.tex")
        return 2

    english = Path(sys.argv[1])
    german = Path(sys.argv[2])
    english_numbers = heading_numbers(english)
    german_numbers = heading_numbers(german)

    if english_numbers != german_numbers:
        print("Language parity check failed.")
        print(f"English sequence: {english_numbers}")
        print(f"German sequence:  {german_numbers}")
        return 1

    print(f"Language parity: OK ({len(english_numbers)} numbered headings)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
