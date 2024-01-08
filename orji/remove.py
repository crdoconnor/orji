import click
from .tempdir import TempDir
from .lookup import Lookup
from .loader import Loader
from pathlib import Path


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
    loader = Loader(temp_dir)
    lookup = Lookup(location)
    item = lookup.load(loader)
    if children:
        item.delete_children()
    else:
        item.delete()
    Path(lookup.filepath).write_text(str(item._org))
    click.echo("Deleted note(s) successfully")
    temp_dir.destroy()
