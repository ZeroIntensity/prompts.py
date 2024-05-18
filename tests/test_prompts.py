from prompts import ask
from io import StringIO
from tempfile import TemporaryFile


def test_ask():
    output = StringIO()

    with TemporaryFile("w+") as file:
        file.write("hello world\r")
        file.flush()
        file.seek(0)
        assert ask("test", output_file=output, input_file=file) == "hello world"

    assert (
        output.getvalue()
        == "\r?\x1b[0m \x1b[1mtest \x1b[1m\x1b[30m›\x1b[0m \x1b[0m\x1b[37m\x1b[0m\x1b[32m\x1b[2m\x1b[4mh\x1b[0m\x1b[32m\x1b[2m\x1b[4me\x1b[0m\x1b[32m\x1b[2m\x1b[4ml\x1b[0m\x1b[32m\x1b[2m\x1b[4ml\x1b[0m\x1b[32m\x1b[2m\x1b[4mo\x1b[0m\x1b[32m\x1b[2m\x1b[4m \x1b[0m\x1b[32m\x1b[2m\x1b[4mw\x1b[0m\x1b[32m\x1b[2m\x1b[4mo\x1b[0m\x1b[32m\x1b[2m\x1b[4mr\x1b[0m\x1b[32m\x1b[2m\x1b[4ml\x1b[0m\x1b[32m\x1b[2m\x1b[4md\x1b[0m\n\x1b[F\x1b[1m\x1b[32m✔\x1b[0m\x1b[0m \x1b[1mtest \x1b[1m\x1b[30m›\x1b[0m \x1b[0m\x1b[32m\x1b[2m\x1b[4mhello world\x1b[0m\n"
    )
