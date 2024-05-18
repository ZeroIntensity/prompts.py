# Click Integration

This is probably what you're all here for! prompts.py lets you drop it's pretty prompts right into an existing CLI using [Click](https://click.palletsprojects.com/en/8.1.x/), with a few limitations. This can be done by passing the `PrettyOption` class to `click.option`.

!!! note

    If you're using Click, you probably have it installed. However, if by some miracle you don't, install prompts.py with the `click` optional dependency:

    ```console
    $ pip install prompts.py[click]
    ```

For example:

```py
from prompts.integration import PrettyOption
import click

@click.command()
@click.option(
    "--name",
    prompt='What is your name?',
    cls=PrettyOption,
)
def main(name: str):
    print(f"Hello, {name}")

if __name__ == "__main__":
    main()

```

This has a few limitations as of now:

-   `hide_input` is unsupported
-   `show_choices` is unsupported
-   `confirmation_prompt` is unsupported
-   `value_proc` is unsupported

However, on the bright side, flags, defaults, and custom prompt strings are all supported!
