# Welcome to prompts.py's documentation!

## Installation

```console
$ pip install prompts.py
```

## Quickstart

```py
from prompts import ask, ValidatorResult

def validate(message: str) -> ValidatorResult:
    if "it" in message:
        return "It is one of the words the knights of Ni! cannot hear!"

    return True

message = ask("...", validate=validate)
```

```py
# Drop in for Click
from prompts.integration import PrettyOption

@click.command()
@click.option("--use-foo", is_flag=True, cls=PrettyOption)
def my_cli(use_foo: bool)
    ...

my_cli()
```

## Inspiration

`prompts.py` was inspired by JavaScript's [prompts](https://www.npmjs.com/package/prompts) library, check it out! This project was also written specifically for powering [view.py](https://github.com/ZeroIntensity/view.py)'s CLI, check it out as well!

You'll notice lots of Monty Python references throughout this documentation! I had fun writing them.
