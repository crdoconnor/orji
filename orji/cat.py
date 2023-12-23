from .note import Note
from pathlib import Path
import click
from .template import Template
from .utils import random_5_digit_number
import shutil
import orgmunge


@click.command()
@click.argument("orgfile")
@click.argument("jinjafile")
@click.option(
    "--indexlookup",
    "indexlookup",
    help="Specify zero-indexed subnote to use e.g. 0/0/4",
)
@click.option(
    "--latexmode",
    is_flag=True,
    show_default=True,
    default=False,
    help="Jinja2 latex mode",
)
@click.option(
    "--module",
    "pymodule",
    help="Specify python module to use in template.",
)
def cat(orgfile, jinjafile, indexlookup, latexmode, pymodule):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    temp_dir = Path(".")
    working_dir = temp_dir / f"{random_5_digit_number()}.tmp"
    working_dir.mkdir()
    munge_parsed = orgmunge.Org(
        org_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )
    notes = Note(munge_parsed.root, working_dir=working_dir)

    if indexlookup is not None:
        notes = notes.from_indexlookup(indexlookup)

    output_text = Template(
        template_text, jinjafile, latexmode=latexmode, pymodule_filename=pymodule
    ).render(notes=notes, root=notes)

    click.echo(output_text)
    shutil.rmtree(working_dir)
