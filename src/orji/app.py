from ._version import __version__
from .note import Note
from pathlib import Path
from orgparse import loads
import traceback
import jinja2
import click
from sys import exit


class Failure(Exception):
    pass


def fail(message):
    raise Failure(message)


@click.command()
@click.argument("orgfile")
@click.argument("jinjafile")
@click.option("-i", "--indexlookup", "indexlookup")
def main(orgfile, jinjafile, indexlookup):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    parsed = loads(org_text)
    notes = Note(parsed)

    if indexlookup is not None:
        notes = notes.from_indexlookup(indexlookup)

    environment = jinja2.Environment(
        undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
    )
    environment.globals["fail"] = fail

    try:
        output_text = environment.from_string(template_text).render(notes=notes)
    except jinja2.exceptions.UndefinedError as error:
        lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
        click.echo(f"Template error on line {lineno} of {jinjafile}: {error}", err=True)
        exit(1)
    except Failure as error:
        lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
        click.echo(f"Failure on line {lineno} of {jinjafile}: {error}", err=True)
        exit(1)

    click.echo(output_text)
