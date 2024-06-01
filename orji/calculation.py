import click
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from pathlib import Path


@click.command()
@click.argument("relative")
def calculation(relative):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)
    write_note = lookup.load(loader)

    headline = write_note.name
    body = write_note.body.text

    if body.startswith("=") and "=" in headline:
        actual_value = eval(body.lstrip("="))
        left_hand_side = headline.split("=")[0]
        write_note.set_name(left_hand_side + "= " + str(actual_value))

    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
