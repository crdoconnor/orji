from .note import Note, OrjiError
from pathlib import Path
from orgparse import loads
import traceback
import jinja2
import click
import imp
import inspect
from sys import exit


class Failure(Exception):
    pass


def fail(message):
    raise Failure(message)


def environment(latexmode, pymodule_filename):
    if latexmode:
        env = jinja2.Environment(
            block_start_string=r"\BLOCK{",
            block_end_string="}",
            variable_start_string=r"\VAR{",
            variable_end_string="}",
            comment_start_string=r"\#{",
            comment_end_string="}",
            line_statement_prefix="%%",
            line_comment_prefix="%#",
            trim_blocks=True,
            autoescape=False,
            undefined=jinja2.StrictUndefined,
            loader=jinja2.BaseLoader,
        )
    else:
        env = jinja2.Environment(
            undefined=jinja2.StrictUndefined, loader=jinja2.BaseLoader
        )

    if pymodule_filename is not None:
        pymodule_filepath = Path(pymodule_filename)

        if not pymodule_filepath.exists():
            click.echo(f"{pymodule_filename} not found", err=True)
            exit(1)

        module_contents = {
            key: item
            for key, item in inspect.getmembers(
                imp.load_source(
                    pymodule_filepath.stem, str(pymodule_filepath.absolute())
                )
            )
            if not key.startswith("_")
        }
        env.globals.update(module_contents)

    env.globals["fail"] = fail
    return env


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
def main(orgfile, jinjafile, indexlookup, latexmode, pymodule):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    parsed = loads(org_text)
    notes = Note(parsed)

    if indexlookup is not None:
        notes = notes.from_indexlookup(indexlookup)

    try:
        output_text = (
            environment(latexmode=latexmode, pymodule_filename=pymodule)
            .from_string(template_text)
            .render(notes=notes, root=notes)
        )
    except jinja2.exceptions.UndefinedError as error:
        lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
        click.echo(f"Template error on line {lineno} of {jinjafile}: {error}", err=True)
        exit(1)
    except jinja2.exceptions.TemplateSyntaxError as error:
        lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
        click.echo(
            f"Template syntax error on line {lineno} of {jinjafile}: {error}", err=True
        )
        exit(1)
    except Failure as error:
        lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
        click.echo(f"Failure on line {lineno} of {jinjafile}: {error}", err=True)
        exit(1)
    except OrjiError as error:
        lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
        click.echo(f"Failure on line {lineno} of {jinjafile}: {error}", err=True)
        exit(1)

    click.echo(output_text)
