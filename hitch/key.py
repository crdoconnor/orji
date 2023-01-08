from hitchstory import StoryCollection
from commandlib import Command, python
from click import argument, group, pass_context
from pathquery import pathquery
import hitchpylibrarytoolkit
from engine import Engine
from path import Path


class Directories:
    gen = Path("/gen")
    key = Path("/src/hitch/")
    project = Path("/src/")
    share = Path("/gen")


DIR = Directories()


@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass


PROJECT_NAME = "orji"

toolkit = hitchpylibrarytoolkit.ProjectToolkit(
    PROJECT_NAME,
    DIR,
)

"""
----------------------------
Non-runnable utility methods
---------------------------
"""


def _storybook(**settings):
    return StoryCollection(
        pathquery(DIR.key / "story").ext("story"), Engine(DIR, **settings)
    )


def _current_version():
    return DIR.project.joinpath("VERSION").bytes().decode("utf8").rstrip()


"""
-----------------
RUNNABLE COMMANDS
-----------------
"""


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story matching keywords.
    """
    _storybook().only_uninherited().shortcut(*keywords).play()


@cli.command()
@argument("pyversion", nargs=1)
@argument("keywords", nargs=-1)
def tver(pyversion, keywords):
    """
    Run story against specific version of Python - e.g. tver 3.7.0 modify multi line
    """
    _storybook().with_params(
        **{"python version": pyversion}
    ).only_uninherited().shortcut(*keywords).play()


@cli.command()
@argument("keywords", nargs=-1)
def rbdd(keywords):
    """
    Run story matching keywords and rewrite story if code changed.
    """
    _storybook(rewrite=True).with_params(
        **{"python version": "3.7.0"}
    ).only_uninherited().shortcut(*keywords).play()


@cli.command()
@argument("filename", nargs=1)
def regressfile(filename):
    """
    Run all stories in filename 'filename' in python 3.7.
    """
    _storybook().with_params(**{"python version": "3.7.0"}).in_filename(
        filename
    ).ordered_by_name().play()


@cli.command()
def regression():
    """
    Run regression testing - lint and then run all tests.
    """
    _lint()
    storybook = _storybook().only_uninherited()
    storybook.with_params(**{"python version": "3.7.0"}).ordered_by_name().play()


@cli.command()
@argument("python_path", nargs=1)
@argument("python_version", nargs=1)
def regression_on_python_path(python_path, python_version):
    """
    Run regression tests - e.g. hk regression_on_python_path /usr/bin/python 3.7.0
    """
    _storybook(python_path=python_path).with_params(
        **{"python version": python_version}
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def checks():
    """
    Run all checks ensure linter, code formatter, tests and docgen all run correctly.

    These checks should prevent code that doesn't have the proper checks run from being merged.
    """
    toolkit.validate_reformatting()
    _lint()
    storybook = _storybook().only_uninherited()
    storybook.with_params(**{"python version": "3.7.0"}).ordered_by_name().play()


@cli.command()
def reformat():
    """
    Reformat using black and then relint.
    """
    toolkit.reformat()


def _lint():
    toolkit.lint()


@cli.command()
def lint():
    """
    Lint project code and hitch code.
    """
    _lint()


@cli.command()
def deploy():
    """
    Deploy to pypi as specified version.
    """
    git = Command("git")
    git("clone", "git@github.com:crdoconnor/orji.git").in_dir(DIR.gen).run()
    project = DIR.gen / "orji"
    version = project.joinpath("VERSION").text().rstrip()
    initpy = project.joinpath("orji", "__init__.py")
    original_initpy_contents = initpy.bytes().decode("utf8")
    initpy.write_text(original_initpy_contents.replace("DEVELOPMENT_VERSION", version))
    python("setup.py", "sdist").in_dir(project).run()
    initpy.write_text(original_initpy_contents)

    # Upload to pypi
    python(
        "-m",
        "twine",
        "upload",
        "dist/{0}-{1}.tar.gz".format("orji", version),
    ).in_dir(project).run()

    # Clean up
    DIR.gen.joinpath("orji").rmtree()


@cli.command()
def docgen():
    """
    Build documentation.
    """
    toolkit.docgen(Engine(DIR))


@cli.command()
def readmegen():
    """
    Build README.md and CHANGELOG.md.
    """
    toolkit.readmegen(Engine(DIR))


@cli.command()
def rerun():
    """
    Rerun last example code block with specified version of Python.
    """
    from commandlib import Command

    version = "3.7.0"
    Command(DIR.gen.joinpath("py{0}".format(version), "bin", "python"))(
        DIR.gen.joinpath("working", "examplepythoncode.py")
    ).in_dir(DIR.gen.joinpath("working")).run()


@cli.command()
def bash():
    """
    Run bash
    """
    from commandlib import Command

    Command("bash").run()


@cli.command()
def build():
    import hitchpylibrarytoolkit

    hitchpylibrarytoolkit.project_build(
        "strictyaml",
        DIR,
        "3.7.0",
        {"ruamel.yaml": "0.16.5"},
    )


if __name__ == "__main__":
    cli()
