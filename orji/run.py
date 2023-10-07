from .note import Note, OrjiError
from pathlib import Path
from orgparse import loads
import traceback
import jinja2
import click
import imp
import inspect
from sys import exit
import stat
import os


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
@click.argument("orgdir")
@click.argument("rundir")
def run(orgdir, rundir):
    orgdir = Path(orgdir)
    rundir = Path(rundir)
    
    assert orgdir.is_dir()
    assert rundir.is_dir()
    assert len(list(orgdir.glob("*.org"))), "orgdir must contain org files"
    assert len(list(rundir.glob("*.sh"))), "rundir must contain sh files"
    
    scripts = {
        script.stem: script.read_text()
        for script in rundir.glob("*.sh")
    }
    env = environment(False, None)
    tmp = Path("/tmp")
    
    for orgfile in orgdir.glob("*.org"):
        for note in loads(Path(orgfile).read_text()).children:
            if note.todo == "TODO":
                for tag in note.tags:
                    if tag in scripts.keys():
                        notebody_path = tmp.joinpath("notebody.txt")
                        notebody_path.write_text(note.body)
                        tmp_script = tmp.joinpath("{}.sh".format(tag))
                        tmp_script.write_text(
                            env.from_string(scripts[tag])
                            .render(notebody=notebody_path)
                        )                        
                        tmp_script.chmod(tmp_script.stat().st_mode | stat.S_IEXEC)
                        os.system(tmp_script)
                        #subprocess.call(["sh", tmp_script])
                        #import web_pdb; web_pdb.set_trace()