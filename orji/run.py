from .note import Note
from pathlib import Path
import click
from click import echo
from sys import exit
import stat
import subprocess
from .template import Template
import orgmunge
from .tempdir import TempDir


@click.command()
@click.argument("orgdir")
@click.argument("rundir")
@click.option(
    "--out",
    help="Output folder. Defaults to current.",
)
@click.option(
    "--multiple/--single",
    help="Output folder. Defaults to current.",
    default=False,
)
def run(orgdir, rundir, out, multiple):
    temp_dir = TempDir()
    temp_dir.create()
    orgdir = Path(orgdir).absolute()
    rundir = Path(rundir).absolute()

    assert orgdir.is_dir()
    assert rundir.is_dir()
    assert len(list(orgdir.glob("*.org"))), "orgdir must contain org files"
    assert len(list(rundir.glob("*.sh"))), "rundir must contain sh files"

    scripts = {script.stem: script.read_text() for script in rundir.glob("*.sh")}

    out_dir = Path("." if out is None else out).absolute()

    assert out_dir.is_dir()
    assert out_dir.exists()

    matching_notes = []

    for orgfile in orgdir.glob("*.org"):
        parsed_munge = orgmunge.Org(
            Path(orgfile).read_text(),
            from_file=False,
            todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
        )

        for note in Note(parsed_munge.root, temp_dir=temp_dir):
            if note.state == "TODO":
                for tag in note.tags:
                    if tag in scripts.keys():
                        matching_notes.append((orgfile, tag, note))

    if len(matching_notes) == 0 and not multiple:
        temp_dir.destroy()
        echo("No scripts were run")
        exit(1)
    elif len(matching_notes) > 1 and not multiple:
        temp_dir.destroy()
        echo("Multiple matching notes use --multiple to run all of them")
        echo("")
        for orgfile, _, note in matching_notes:
            echo(f"{orgfile}: {note.indexlookup}: {note.name}")
        exit(1)
    else:
        for orgfile, tag, note in matching_notes:
            rendered_script = Template(scripts[tag], f"{tag}.sh").render(
                notebody=temp_dir.tempfile(str(note.body), filename="notebody.txt"),
                orgfile=orgfile,
                note=note,
                tmp=temp_dir.working_dir,
                out=out_dir,
                rundir=rundir,
                orgdir=orgdir,
            )
            tmp_script = temp_dir.tempfile(rendered_script, filename=f"{tag}.sh")
            tmp_script.chmod(tmp_script.stat().st_mode | stat.S_IEXEC)
            return_code = subprocess.call(["bash", "-e", tmp_script])
            if return_code != 0:
                print(f"\n\nERROR running {tag}.sh in {temp_dir.working_dir}")
                exit(return_code)
        temp_dir.destroy()
