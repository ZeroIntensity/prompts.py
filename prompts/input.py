import sys
from io import StringIO
from typing import IO, Any, Sequence

from colorama import Fore, Style

from ._getch import getch
from ._styles import ARROW, BACKSPACE, CTRL_C, ITALIC, left

__all__ = ("take_input",)


def take_input(
    file: IO[str] | None = None,
    *,
    output: IO[str] | None = None,
    autocomplete: Sequence[str] | None = None,
    min_autocomplete_chars: int = 2,
    initial: str | None = None,
    initial_color: str = Fore.BLACK + Style.BRIGHT + ITALIC,
    color_sequence: str = Fore.WHITE,
) -> str:
    buffer = StringIO()
    slice: str | None = None
    file = file or sys.stdin
    output = output or sys.stdout
    first_iteration = True

    def write(*messages: Any, nl: bool = False) -> None:
        print(
            *messages,
            end="" if not nl else "\n",
            flush=True,
            file=output,
        )

    if initial:
        write(initial_color + initial + Style.RESET_ALL + left(len(initial)))

    while True:
        key = getch(file)
        if first_iteration and initial:
            write(" " * len(initial) + left(len(initial)))

        first_iteration = False
        bufsize = buffer.tell()
        if (bufsize + 1 > min_autocomplete_chars) and autocomplete:
            val = buffer.getvalue() + key
            found = False

            for item in autocomplete:
                if item.startswith(val):
                    slice = item[bufsize:]
                    write(
                        Style.RESET_ALL
                        + ITALIC
                        + Style.BRIGHT
                        + Fore.BLACK
                        + slice
                        + Style.RESET_ALL
                    )

                    for _ in slice:
                        write("\b")

                    found = True
                    break

            if (not found) and slice:
                write(" " * len(slice))
                write(left(len(slice)))

        if key == CTRL_C:
            raise KeyboardInterrupt

        if key == ARROW:
            continue

        if (key == "\t") and slice:
            write(slice[1:])
            buffer.write(slice[1:])
            continue

        if key == BACKSPACE:
            index = bufsize - 1
            if index < 0:
                continue

            buffer.truncate(index)
            buffer.seek(index)
            if slice:
                write(" " * len(slice))
                write("\b" * len(slice))

            write("\b \b")
            continue

        if key == "\r":
            write("\n")
            break

        write(color_sequence + key + Style.RESET_ALL)
        buffer.write(key)

    return buffer.getvalue()
