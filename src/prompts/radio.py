from __future__ import annotations
import sys
from typing import IO, Literal, Sequence

from colorama import Fore, Style

from ._getch import getch
from ._styles import CTRL_C, PREVIOUS_FIRST, UNDERLINE, left
from .prompt import Prompt

__all__ = ("radio", "ask_radio", "confirm", "ask_confirm")


def radio(
    items: Sequence[str],
    *,
    multi_line: bool = False,
    input_file: IO[str] | None = None,
    output_file: IO[str] | None = None,
    selected_color: str = Fore.GREEN + Style.DIM + UNDERLINE,
    transient: bool = False,
) -> int:
    """
    Display a radio selection.

    Args:
        items: Sequence of available selections. Must have at least 2 values.
        input_file: File descriptor to read input from. `sys.stdin` by default.
        output_file: File descriptor to write output to. `sys.stdout` by default.
        selected_color: Color to use for selected values. Green by default.
        transient: Whether to delete the radio selection after it's done.

    Raises:
        KeyboardInterrupt: User pressed CTRL+C

    Returns:
        Index of the selected item.
    """
    input_file = input_file or sys.stdin
    output_file = output_file or sys.stdout
    selected = 0

    if len(items) < 2:
        raise ValueError("items must have a length of at least 2")

    def render_questions():
        if multi_line:
            for index, question in enumerate(items):
                if selected == index:
                    print(
                        f" - {selected_color}{question}{Style.RESET_ALL}",
                        flush=True,
                        file=output_file,
                    )
                else:
                    print(f" - {question}", flush=True, file=output_file)
        else:
            for index, question in enumerate(items):
                color = selected_color if index == selected else ""
                print(
                    f"{color}{question}{Style.RESET_ALL}",
                    flush=True,
                    end="",
                    file=output_file,
                )

                if index != len(items) - 1:
                    print(
                        f"{Style.BRIGHT}{Fore.BLACK} / {Style.RESET_ALL}",
                        flush=True,
                        end="",
                        file=output_file,
                    )

    render_questions()
    item_sum: int = 0

    if not multi_line:
        for i in items:
            item_sum += len(i) + 3

        item_sum -= 3

    while True:
        key = getch(input_file)

        if key == CTRL_C:
            raise KeyboardInterrupt

        if key in {"A", "D"}:
            if selected != 0:
                selected -= 1
            else:
                continue
        elif key in {"B", "C"}:
            if selected != len(items) - 1:
                selected += 1
            else:
                continue
        elif key == "\r":
            if transient:
                print(
                    left(item_sum) + " " * item_sum + left(item_sum),
                    end="",
                    flush=True,
                    file=output_file,
                )
            if not multi_line:
                print(file=output_file)

            return selected
        else:
            continue

        if multi_line:
            for _ in items:
                print(
                    PREVIOUS_FIRST,
                    end="",
                    flush=True,
                    file=output_file,
                )
        else:
            print(left(item_sum), end="", flush=True, file=output_file)

        render_questions()


def ask_radio(
    question: str,
    items: Sequence[str],
    *,
    input_file: IO[str] | None = None,
    output_file: IO[str] | None = None,
    selected_color: str = Fore.GREEN + Style.DIM + UNDERLINE,
) -> int:
    """
    Display a radio selection with a prompt.

    Args:
        items: Sequence of available selections. Must have at least 2 values.
        input_file: File descriptor to read input from. `sys.stdin` by default.
        output_file: File descriptor to write output to. `sys.stdout` by default.
        selected_color: Color to use for selected values. Green by default.

    Raises:
        KeyboardInterrupt: User pressed CTRL+C

    Returns:
        Index of the selected item.
    """
    with Prompt(question, output_file=output_file) as prompt:
        index = radio(
            items,
            input_file=input_file,
            output_file=output_file,
            selected_color=selected_color,
            transient=True,
        )
        prompt.answer = items[index]
        prompt.done()
        return index


def confirm(
    *,
    default: Literal[True, False] = True,
    input_file: IO[str] | None = None,
    output_file: IO[str] | None = None,
    selected_color: str = Fore.GREEN + Style.DIM + UNDERLINE,
) -> bool:
    """
    Get a yes or no value from the user, as a boolean.

    Args:
        default: Option to be the selected value at first.
        input_file: File descriptor to read input from. `sys.stdin` by default.
        output_file: File descriptor to write output to. `sys.stdout` by default.
        selected_color: Color to use for selected values. Green by default.

    Raises:
        KeyboardInterrupt: User pressed CTRL+C

    Returns:
        `True` if yes was selected, `False` if no was selected.
    """
    seq = ["Yes", "No"] if default is True else ["No", "Yes"]
    index = radio(
        seq,
        input_file=input_file,
        output_file=output_file,
        selected_color=selected_color,
        transient=True,
    )
    return seq[index] == "Yes"


def ask_confirm(
    question: str,
    *,
    default: Literal[True, False] = True,
    input_file: IO[str] | None = None,
    output_file: IO[str] | None = None,
    selected_color: str = Fore.GREEN + Style.DIM + UNDERLINE,
) -> bool:
    """
    Get a yes or no value from the user, with a prompt.

    Args:
        question: Prompt to display.
        default: Option to be the selected value at first.
        input_file: File descriptor to read input from. `sys.stdin` by default.
        output_file: File descriptor to write output to. `sys.stdout` by default.
        selected_color: Color to use for selected values. Green by default.

    Raises:
        KeyboardInterrupt: User pressed CTRL+C

    Returns:
        `True` if yes was selected, `False` if no was selected.
    """
    with Prompt(question, output_file=output_file) as prompt:
        value = confirm(
            default=default,
            input_file=input_file,
            output_file=output_file,
            selected_color=selected_color,
        )
        prompt.answer = "Yes" if value else "No"
        prompt.done()
        return value
