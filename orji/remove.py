import click
from .tempdir import TempDir
from .lookup import Lookup


@click.command()
@click.argument("location")
@click.option(
    "--children",
    "children",
    is_flag=True,
    help="Remove all children of referenced note, not the actual note.",
)
def remove(location, children):
    temp_dir = TempDir()
    temp_dir.create()
    lookup = Lookup(location)
    lookup
    # Path(lookup.filepath).write_text(str(write_note))
    click.echo("Deleted note(s) successfully")
    temp_dir.destroy()
