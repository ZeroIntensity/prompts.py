from __future__ import annotations
import os
import sys
from typing import IO


def _handle_read(val: str) -> str:
    if val == "":
        raise EOFError

    return val


if os.name == "nt":
    import msvcrt

    def getch(file: IO[str]):
        if file is sys.stdin:
            return msvcrt.getwch()
        return _handle_read(file.read(1))

else:
    import termios
    import tty

    def getch(file: IO[str]):
        fd = file.fileno()
        try:
            old_settings = termios.tcgetattr(fd)
        except termios.error:
            # running in a file stream or something similar, just read
            return _handle_read(file.read(1))

        try:
            tty.setraw(file.fileno())
            ch = file.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch
