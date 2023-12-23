from .note import Note
from pathlib import Path
import click
from .template import Template
import orgmunge
from .tempdir import TempDir


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
    temp_dir = TempDir()
    temp_dir.create()
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    munge_parsed = orgmunge.Org(
        org_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )
    notes = Note(munge_parsed.root, temp_dir=temp_dir)

    if indexlookup is not None:
        notes = notes.from_indexlookup(indexlookup)

    output_text = Template(
        template_text, jinjafile, latexmode=latexmode, pymodule_filename=pymodule
    ).render(notes=notes, root=notes)

    click.echo(output_text)
    temp_dir.destroy()
