from .note import Note
from pathlib import Path
from orgparse import loads
import click
from .template import Template
from .utils import random_5_digit_number
import shutil
import orgmunge


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
def cat(orgfile, jinjafile, indexlookup, latexmode, pymodule):
    org_text = Path(orgfile).read_text()
    template_text = Path(jinjafile).read_text()
    temp_dir = Path(".")
    working_dir = temp_dir / f"{random_5_digit_number()}.tmp"
    working_dir.mkdir()
    munge_parsed = orgmunge.Org(
        org_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )
    parsed = loads(org_text)
    notes = Note(munge_parsed.root, working_dir=working_dir)

    if indexlookup is not None:
        notes = notes.from_indexlookup(indexlookup)

    output_text = Template(
        template_text, jinjafile, latexmode=latexmode, pymodule_filename=pymodule
    ).render(notes=notes, root=notes)

    # try:
    #     output_text = (
    #         environment(latexmode=latexmode, pymodule_filename=pymodule)
    #         .from_string(template_text)
    #         .render(notes=notes, root=notes)
    #     )
    # except jinja2.exceptions.UndefinedError as error:
    #     lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
    #     click.echo(f"Template error on line {lineno} of {jinjafile}: {error}", err=True)
    #     exit(1)
    # except jinja2.exceptions.TemplateSyntaxError as error:
    #     lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
    #     click.echo(
    #         f"Template syntax error on line {lineno} of {jinjafile}: {error}", err=True
    #     )
    #     exit(1)
    # except jinja2.exceptions.TemplateRuntimeError as error:
    #     lineno = traceback.extract_tb(error.__traceback__)[-1].lineno
    #     click.echo(
    #         f"Template runtime error on line {lineno} of {jinjafile}: {error}", err=True
    #     )
    #     exit(1)
    # except Failure as error:
    #     lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
    #     click.echo(f"Failure on line {lineno} of {jinjafile}: {error}", err=True)
    #     exit(1)
    # except OrjiError as error:
    #     lineno = traceback.extract_tb(error.__traceback__)[-2].lineno
    #     click.echo(f"Failure on line {lineno} of {jinjafile}: {error}", err=True)
    #     exit(1)

    click.echo(output_text)
    shutil.rmtree(working_dir)
