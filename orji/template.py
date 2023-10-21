from .note import OrjiError
import jinja2
import click
import imp
import traceback
from sys import exit
from pathlib import Path
import inspect


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


class Template:
    def __init__(
        self, template_text, jinjafile, latexmode=None, pymodule_filename=None
    ):
        self._template_text = template_text
        self._jinjafile = jinjafile
        self._latexmode = latexmode
        self._pymodule_filename = pymodule_filename
        self._env = environment(latexmode, pymodule_filename)

    def render(self, **vars):
        try:
            return self._env.from_string(self._template_text).render(**vars)
        except jinja2.exceptions.UndefinedError as error:
            lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
            click.echo(
                f"Template error on line {lineno} of {self._jinjafile}: {error}",
                err=True,
            )
            exit(1)
        except jinja2.exceptions.TemplateSyntaxError as error:
            lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
            click.echo(
                f"Template syntax error on line {lineno} of {self._jinjafile}: {error}",
                err=True,
            )
            exit(1)
        except jinja2.exceptions.TemplateRuntimeError as error:
            lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
            click.echo(
                f"Template runtime error on line {lineno} of {self._jinjafile}: {error}",
                err=True,
            )
            exit(1)
        except Failure as error:
            lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
            click.echo(
                f"Failure on line {lineno} of {self._jinjafile}: {error}", err=True
            )
            exit(1)
        except OrjiError as error:
            lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
            click.echo(
                f"Failure on line {lineno} of {self._jinjafile}: {error}", err=True
            )
            exit(1)
