import os
import sys
from typing import IO

if os.name == "nt":
    import msvcrt

    def getch(file: IO[str]):
        if file is sys.stdin:
            return msvcrt.getwch()
        return file.read(1)

else:
    import termios
    import tty

    def getch(file: IO[str]):
        fd = file.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(file.fileno())
            ch = file.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        return ch
