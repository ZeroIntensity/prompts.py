from __future__ import annotations

from typing import IO, Callable, Union

from colorama import Fore, Style
from typing_extensions import TypeAlias

from ._styles import UNDERLINE, ITALIC
from .input import take_input
from .prompt import Prompt

ValidatorResult: TypeAlias = Union[str, bool]
Validator: TypeAlias = Callable[[str], ValidatorResult]

__all__ = ("ask", "ValidatorResult", "Validator")


def ask(
    question_str: str,
    *,
    default: str | None = None,
    initial: str | None = None,
    input_file: IO[str] | None = None,
    output_file: IO[str] | None = None,
    validate: Validator | list[Validator] | None = None,
    default_invalid: str = "Invalid response.",
) -> str | None:
    """
    Ask a question with a prompt.

    Args:
        question_str: Prompt to show the user.
        initial: Initial value, as shown in `take_input`.
        input_file: File descriptor to read input from. `sys.stdin` by default.
        output_file: File descriptor to write output to. `sys.stdout` by default.
        validate: Validator(s) to be used for validation of the input.
        default_invalid: Default message to show the user if a validator returns `False`.

    Raises:
        KeyboardInterrupt: User pressed CTRL+C

    Returns:
        The inputted value.
    """
    validators = (
        validate if isinstance(validate, list) else [validate] if validate else []
    )

    with Prompt(question_str, output_file=output_file) as prompt:
        while True:
            if default and (not initial):
                initial = default

            text = take_input(
                input_file,
                output=output_file,
                initial=initial,
                color_sequence=Fore.GREEN + Style.DIM + UNDERLINE,
                initial_color=(
                    Fore.BLACK + Style.BRIGHT + ITALIC
                    if not prompt.answer
                    else Fore.RED + Style.BRIGHT + UNDERLINE
                ),
            )
            if (text == "") and default:
                text = default
            error: str | bool | None = None
            for validator in validators:
                failed_message = validator(text)

                if failed_message is not True:
                    if failed_message is False:
                        error = default_invalid
                    else:
                        error = failed_message

            prompt.answer = text
            if error:
                prompt.error(error)
                initial = text
            else:
                prompt.done()
                return text
