from .cat import cat
import click


@click.group()
def cli():
    pass


cli.add_command(cat)
