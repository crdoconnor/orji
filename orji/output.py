from pathlib import Path
import click
from .template import Template
from .tempdir import TempDir
from .lookup import Lookup
from .loader import Loader
from .note import Note


@click.command()
@click.argument("orglookup")
@click.argument("jinjafile")
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
def output(orglookup, jinjafile, latexmode, pymodule):
    lookup = Lookup(orglookup)
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir, multiple_files_ok=True)
    template_text = Path(jinjafile).read_text()
    notes = lookup.load(loader)

    if isinstance(notes, Note):
        output_text = Template(
            template_text, jinjafile, latexmode=latexmode, pymodule_filename=pymodule
        ).render(note=notes, notes=notes, root=notes, at=notes.at, has=notes.has)
    else:
        output_text = Template(
            template_text, jinjafile, latexmode=latexmode, pymodule_filename=pymodule
        ).render(orgfiles=notes)

    click.echo(output_text)
    temp_dir.destroy()
