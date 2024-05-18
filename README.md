# prompts.py

## Beautiful prompts for Python.

[![PyPI - Version](https://img.shields.io/pypi/v/prompts.svg)](https://pypi.org/project/prompts.py)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/prompts.svg)](https://pypi.org/project/prompts.py)

_Inspired by the [prompts](https://www.npmjs.com/package/prompts) package on NPM. This project was written specifically for [view.py](https://github.com/ZeroIntensity/view.py)_

---

## Example

![Alt Text](https://raw.githubusercontent.com/ZeroIntensity/prompts.py/master/assets/example.gif)

```py
from prompts import ask, ValidatorResult

def validate(name: str) -> ValidatorResult:
    if name == "andrew":
        return "You're not allowed here, buddy!"

    return True

ask("What's your name?", validate=validate)
```

## Features

-   Fully typed
-   Extendable
-   Drop-in support for [Click](https://click.palletsprojects.com/)

### Click Example

```py
from prompts.integration import PrettyOption
import click

@click.command()
@click.option(
    "--name",
    default="Peter",
    prompt=True,
    cls=PrettyOption,  # Enable prompts.py inputs!
)
def main(name: str):
    ...

if __name__ == "__main__":
    main()
```

## Installation

```console
$ pip install prompts.py
```

## License

`prompts.py` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
