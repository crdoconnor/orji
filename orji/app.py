from .cat import cat
from .run import run
import click


@click.group()
def cli():
    pass


cli.add_command(cat)
cli.add_command(run)
