from .cat import cat
from .run import run
from .insert import insert
import click


@click.group()
def cli():
    pass


cli.add_command(cat)
cli.add_command(run)
cli.add_command(insert, name="in")
