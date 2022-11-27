from ._version import __version__
from pathlib import Path
from orgparse import loads
import jinja2
import click


@click.command()
@click.argument('orgfile')
@click.argument('jinjafile')
def main(orgfile, jinjafile):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    notes = loads(org_text)[1:]
    output_text = jinja2.Template(template_text).render(notes=notes)
    
    click.echo(output_text)
