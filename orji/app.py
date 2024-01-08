from .output import output
from .run import run
from .insert import insert
from .remove import remove
import click


@click.group()
def cli():
    pass


cli.add_command(output, name="out")
cli.add_command(run)
cli.add_command(insert, name="in")
cli.add_command(remove, name="rm")
