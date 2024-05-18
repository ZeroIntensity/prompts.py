from __future__ import annotations

from typing import IO, Callable, Union

from colorama import Fore, Style
from typing_extensions import TypeAlias

from ._styles import UNDERLINE
from .input import take_input
from .prompt import Prompt

ValidatorResult: TypeAlias = Union[str, bool]
Validator: TypeAlias = Callable[[str], ValidatorResult]

__all__ = ("ask", "ValidatorResult", "Validator")


class InvalidPrompt(BaseException):
    def __init__(self, message: str) -> None:
        self.message = message


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
    validators = (
        validate
        if isinstance(validate, list)
        else [validate] if validate else []
    )

    while True:
        with Prompt(question_str, output_file=output_file) as prompt:
            if default and (not initial):
                initial = default

            text = take_input(
                input_file,
                output=output_file,
                initial=initial,
                color_sequence=Fore.GREEN + Style.DIM + UNDERLINE,
            )
            if (text == "") and default:
                text = default
            error: str | bool | None = None
            for validator in validators:
                try:
                    failed_message = validator(text)
                except InvalidPrompt as e:
                    failed_message = e.message

                if failed_message is not True:
                    if not failed_message:
                        error = default_invalid

                    error = failed_message

            prompt.answer = text
            if error:
                prompt.error(error)
            else:
                prompt.done()
                return text
