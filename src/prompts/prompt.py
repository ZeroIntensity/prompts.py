from __future__ import annotations

import sys
from typing import IO, Any

from colorama import Fore, Style, init
from typing_extensions import Final, Self

from ._styles import BOLD, CLEAR, PREVIOUS_FIRST, UNDERLINE, right

__all__ = ("Prompt",)


init()


_ARROW: Final[str] = f"{Style.BRIGHT}{Fore.BLACK}›{Style.RESET_ALL}"
_CHECK: Final[str] = f"{Style.BRIGHT}{Fore.GREEN}✔{Style.RESET_ALL}"
_ERROR: Final[str] = f"{Style.BRIGHT}{Fore.RED}✗{Style.RESET_ALL}"


class Prompt:
    """Low level prompt API."""

    def __init__(
        self,
        prompt_str: str,
        *,
        output_file: IO[str] | None = None,
        prompt_char: str = "?",
    ) -> None:
        self.prompt_str = prompt_str
        self.output_file = output_file or sys.stdout
        self.prompt_char = prompt_char
        self.answer: str = ""
        self.answer_color = Fore.WHITE
        self._shown_error = False

    def write(self, *messages: Any, nl: bool = False) -> None:
        print(
            *messages,
            flush=True,
            end="" if not nl else "\n",
            file=self.output_file,
        )

    def _make_prompt_str(self) -> str:
        return (
            f"{self.prompt_char}{Style.RESET_ALL}"
            + f" {BOLD}{self.prompt_str} {_ARROW} {Style.RESET_ALL}"
            + f"{self.answer_color}{self.answer}{Style.RESET_ALL}"
        )

    def render(self) -> str:
        prompt_str = self._make_prompt_str()
        self.write("\r" + prompt_str)
        return prompt_str

    def error(
        self,
        error: str,
        *,
        color: str = Style.BRIGHT + Fore.RED,
    ) -> None:
        self._shown_error = True
        self.prompt_char = _ERROR
        self.answer_color = Fore.RED + Style.BRIGHT + UNDERLINE
        self.write(PREVIOUS_FIRST + CLEAR)
        self.render()
        self.write(f"\n\r{_ARROW} {color}{error}{Style.RESET_ALL}")
        self.write(PREVIOUS_FIRST + right(len(self.prompt_str) + 5))

    def done(
        self,
    ) -> None:
        self.prompt_char = _CHECK
        self.answer_color = Fore.GREEN + Style.DIM + UNDERLINE
        prompt_str = self._make_prompt_str()
        self.write(
            PREVIOUS_FIRST + prompt_str,
            nl=True,
        )

    def finish(self) -> None:
        if self._shown_error:
            self.write(PREVIOUS_FIRST + CLEAR)

    def __enter__(self) -> Self:
        self.render()
        return self

    def __exit__(self, *_) -> None:
        self.finish()
