from .note import Note
from pathlib import Path
import click
from .template import Template
import orgmunge
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup


@click.command()
@click.argument("jinjafile")
@click.argument("relative")
@click.argument("location")
@click.option(
    "--text",
    "textfile",
    help="Put file contents into {{ text }}",
)
def insert(jinjafile, relative, location, textfile):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(location)
    template_text = Path(jinjafile).read_text()
    output_text = Template(template_text, jinjafile).render(
        text=Path(textfile).read_text()
    )
    chunk_to_insert = orgmunge.Org(
        output_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )

    write_note = lookup.load(loader)
    if relative == "above":
        for note in chunk_to_insert.root.children:
            write_note._node.add_child(note)
    elif relative == "below":
        for note in chunk_to_insert.root.children:
            write_note._node.add_child(note)
    else:
        raise NotImplementedError("f{relative} not implemented")
    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
