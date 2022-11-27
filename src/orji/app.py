from ._version import __version__
from .note import Note
from pathlib import Path
from orgparse import loads
import jinja2
import click


@click.command()
@click.argument("orgfile")
@click.argument("jinjafile")
def main(orgfile, jinjafile):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    parsed = loads(org_text)
    notes = Note(parsed)

    environment = jinja2.Environment(
        undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
    )

    output_text = environment.from_string(template_text).render(notes=notes)

    click.echo(output_text)
