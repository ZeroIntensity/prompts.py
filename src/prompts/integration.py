from __future__ import annotations
from typing import Any

import click
from click.types import convert_type

from .question import ValidatorResult, ask
from .radio import ask_confirm, ask_radio

__all__ = ("PrettyOption",)


def prompt(
    text: str,
    default: Any | None = None,
    type: click.ParamType | Any | None = None,
) -> Any:
    if isinstance(type, click.Choice):
        index = ask_radio(text, type.choices)
        return type.choices[index]

    if type is click.BOOL:
        assert isinstance(default, bool)
        return ask_confirm(text, default=default)

    value_proc = convert_type(type, default)
    result: Any = None

    def validate(value: Any) -> ValidatorResult:
        try:
            nonlocal result
            result = value_proc(value)
        except click.UsageError as e:
            return f"{e.message}"

        return True

    ask(text, validate=validate, default=str(default) if default else None)
    return result


class PrettyOption(click.Option):
    """Option class for Click integration."""

    def prompt_for_value(self, ctx: click.Context) -> Any:
        assert self.prompt is not None
        return prompt(self.prompt, self.default, self.type)
