from .note import Note
from pathlib import Path
import click
from .template import Template
import orgmunge
from .tempdir import TempDir
from .loader import Loader


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
    template_text = Path(jinjafile).read_text()
    output_text = Template(template_text, jinjafile).render(
        text=Path(textfile).read_text()
    )
    chunk_to_insert = orgmunge.Org(
        output_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )

    write_file = location.split(".org/")[0] + ".org"
    _ = location.split(".org/")[1]

    write_parsed = orgmunge.Org(
        Path(write_file).read_text(),
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )
    write_notes = Note(write_parsed.root, loader=loader)
    if relative == "above":
        for note in chunk_to_insert.root.children:
            write_notes._node.add_child(note)
    elif relative == "below":
        for note in chunk_to_insert.root.children:
            write_notes._node.add_child(note)
    else:
        raise NotImplementedError("f{relative} not implemented")
    write_parsed.write(write_file)
    click.echo("Written note successfully")
    temp_dir.destroy()
