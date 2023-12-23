from .note import Note
from pathlib import Path
import click
from .template import Template
from .utils import random_5_digit_number
import orgmunge


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
    template_text = Path(jinjafile).read_text()
    output_text = Template(template_text, jinjafile).render(
        text=Path(textfile).read_text()
    )
    temp_dir = Path(".")
    working_dir = temp_dir / f"{random_5_digit_number()}.tmp"
    working_dir.mkdir()

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
    write_notes = Note(write_parsed.root, working_dir=working_dir)
    chunk_to_insert.initial_body = ""
    write_notes._node.add_child(chunk_to_insert.root)
    write_parsed.initial_body = ""
    write_parsed.write(write_file)
    click.echo("Written note successfully")
