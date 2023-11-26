from .note import Note
from pathlib import Path
from orgparse import loads
import click
from click import echo
from sys import exit
import stat
import subprocess
from .utils import random_5_digit_number
import shutil
from .template import Template
import orgmunge
import os


@click.command()
@click.argument("orgdir")
@click.argument("rundir")
@click.option(
    "--out",
    help="Output folder. Defaults to current.",
)
def run(orgdir, rundir, out):
    tmp = os.getenv("ORJITMP")
    orgdir = Path(orgdir).absolute()
    rundir = Path(rundir).absolute()

    assert orgdir.is_dir()
    assert rundir.is_dir()
    assert len(list(orgdir.glob("*.org"))), "orgdir must contain org files"
    assert len(list(rundir.glob("*.sh"))), "rundir must contain sh files"

    scripts = {script.stem: script.read_text() for script in rundir.glob("*.sh")}

    assert (
        len(list(name for name in scripts.keys() if "-" in name)) == 0
    ), "Do not use dashes in script files"

    temp_dir = Path("." if tmp is None else tmp).absolute()
    out_dir = Path("." if out is None else out).absolute()

    assert temp_dir.is_dir()
    assert temp_dir.exists()
    assert out_dir.is_dir()
    assert out_dir.exists()
    working_dir = temp_dir / f"{random_5_digit_number()}.tmp"
    working_dir.mkdir()

    script_run = False

    for orgfile in orgdir.glob("*.org"):
        parsed_munge = orgmunge.Org(
            Path(orgfile).read_text(),
            from_file=False,
            todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
        )

        for note in Note(parsed_munge.root, working_dir=working_dir):
            if note.state == "TODO":
                for tag in note.tags:
                    if tag in scripts.keys():
                        script_run = True

                        notebody_path = working_dir.joinpath("notebody.txt")
                        notebody_path.write_text(str(note.body))
                        tmp_script = working_dir.joinpath("{}.sh".format(tag))

                        rendered_script = Template(scripts[tag], f"{tag}.sh").render(
                            notebody=notebody_path,
                            orgfile=orgfile,
                            note=note,
                            tmp=working_dir,
                            out=out_dir,
                            rundir=rundir,
                            orgdir=orgdir,
                        )

                        tmp_script.write_text(rendered_script)
                        tmp_script.chmod(tmp_script.stat().st_mode | stat.S_IEXEC)
                        return_code = subprocess.call(["bash", "-e", tmp_script])
                        if return_code != 0:
                            print(f"\n\nERROR running {tag}.sh in {working_dir}")
                            exit(return_code)

    shutil.rmtree(working_dir)
    if not script_run:
        echo("No scripts were run")
        exit(1)
