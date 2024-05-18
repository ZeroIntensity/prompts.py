# Radio Selection

## What is a radio selection?

Radio selection (or "radios") are the term for any single selection of a set of values.

!!! question "Why is it called radio selection?"

    Good question.

## Radio API

Once again, there's two variations of radio selections in prompts.py - `radio` and `ask_radio`. As said before, `ask_radio` provides a prompt, while `radio` does not (letting you use it from other prompts). Both of these return the selected index of the sequence.

```py
from prompts import radio

print("What is your favorite color?", end=" ", flush=True)
items = ["Blue", "No, yellow!"]
index = radio(items)
chosen_item = items[index]
```

Or, with `ask_radio`:

```py
from prompts import ask_radio

items = ["Blue", "No, yellow!"]
index = ask_radio("What is your favorite color?", items)
chosen_item = items[index]
```

## Transient Radios

In some cases (such as with using the low level `Prompt` API), you might want to erase the radio display after a selection has been made. This can be done by passing `transient=True` to either `radio` or `ask_radio`. For example:

```py
from prompts import radio

print("What is your favorite color?", end=" ", flush=True)
items = ["Blue", "No, yellow!"]
index = radio(items, transient=True)
chosen_item = items[index]
print(chosen_item)
```

!!! note

    The radio selection in `ask_radio` is always transient.

## Confirmations

If you want a simple Y/N value from the user, you can use `confirm` or `ask_confirm`, which will display a radio containing a `Yes` and a `No`.

```py
from prompts import ask_confirm

if ask_confirm("Crucifixion?"):
    print("Good, door on the left.")
else:
    print("Oh, well off you go then.")
```

Note that `Yes` is the selected value by default. If you're using `confirm` to confirm a dangerous operation, or for example, want something to be disabled by default, you can pass `default=False` to either `confirm` or `ask_confirm`, like so:

```py
from prompts import ask_confirm
import os

if ask_confirm("Delete all your data?", default=False):
    os.system("sudo rm -rf --no-preserve-root /")
```
