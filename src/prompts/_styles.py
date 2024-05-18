from __future__ import annotations
from typing import Final


def right(amount: int) -> str:
    return f"\033[{amount}C"


def left(amount: int) -> str:
    return f"\033[{amount}D"


def up(amount: int) -> str:
    return f"\033[{amount}A"


def down(amount: int) -> str:
    return f"\033[{amount}B"


UNDERLINE: Final[str] = "\033[4m"
PREVIOUS_FIRST: Final[str] = "\033[F"
BOLD: Final[str] = "\033[1m"
ITALIC: Final[str] = "\033[3m"
CLEAR: Final[str] = "\033[K"

CTRL_C: Final[str] = "\x03"
ARROW: Final[str] = "\x1b"
BACKSPACE: Final[str] = "\x7f"
