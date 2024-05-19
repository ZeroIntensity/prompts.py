# Asking Prompts

## Low vs High Level

prompts.py has a focus on extendability, so there are two ways use each function - the low level variation, and the high level `ask_` variation. `ask_` functions will include the prompt, as shown in the [README](https://github.com/ZeroIntensity/prompts.py), and the low level version will do it bare.

For example, `take_input` is considered to be low level, while `ask` is high level. Speaking of which, what do both of those do?

`take_input` is similar to Python's `input`, but has some fancy abilities, such as autocomplete:

```py
from prompts import take_input

print("My command interpreter!")

while True:
    print("> ", end="", flush=True)
    message = take_input(autocomplete=["help", "echo", "ls"])
```

But, as stated earlier, `take_input` does not display a prompt. If you want the fancy prompt, use `ask`:

```py
from prompts import ask

message = ask("What's so funny about Biggus Dickus?")
```

## Validators

`ask` can take validators, which will display an error message alongside the prompt when they don't pass. `ask` can take a single validator, or a list of them:

```py
from prompts import ask, ValidatorResult

def validate(content: str) -> ValidatorResult:
    return True

message = ask("This will never fail!", validate=validate)
```

A validator should return `True` if the content is valid, and return a `str` or `False` otherwise. If it's a `str`, the string is displayed as an error, and the default value is used otherwise (specified via the `default_invalid` parameter):

```py
from prompts import ask, ValidatorResult

def validate(content: str) -> ValidatorResult:
    if content in {"bread", "apples", "very small rocks"}:
        return "No, no"
    return True

message = ask("What floats on water apart from wood?", validate=validate)
```

## Prompt API

prompts.py provides a lower level prompt API, which is what all the prompt functions use. It's unstable, though. Do not expect API stability!

It comes with a `Prompt` class that acts as a context manager, but if you would like to use it manually, make sure to call `render` initially and call `finish` at the end. To specify an inputted value to the prompt, set `answer`.

!!! warning

    Some wacky behavior can occur if you add extra newlines between prompt API calls!

```py
from prompts import Prompt

with Prompt("My prompt...") as prompt:
    prompt.answer = "My answer..."
    prompt.done()  # Mark the prompt as a success!
```
