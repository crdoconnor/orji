from hitchstory import StoryCollection
from pathquery import pathquery
from click import argument, group, pass_context
import hitchpylibrarytoolkit
from engine import Engine
from commandlib import Command, CommandError
import sys


toolkit = hitchpylibrarytoolkit.ProjectToolkitV2(
    "OrJi",
    "orji",
    "crdoconnor/orji",
    image="",
)


@group(invoke_without_command=True)
@pass_context
def cli(ctx):
    """Integration test command line interface."""
    pass


DIR = toolkit.DIR


def _doctests(python_path):
    try:
        Command(python_path)(
            "-m", "doctest", "-v", DIR.project.joinpath("orji", "utils.py")
        ).in_dir(DIR.project.joinpath("orji")).run()
    except CommandError:
        sys.exit(1)


def _storybook(**settings):
    return StoryCollection(pathquery(DIR.key).ext("story"), Engine(DIR, **settings))


def _current_version():
    return DIR.project.joinpath("VERSION").text().rstrip()


def _devenv():
    return toolkit.devenv()


@cli.command()
def doctests():
    """
    Run doctests in utils.py in latest version.
    """
    _doctests(_devenv().python_path)


@cli.command()
@argument("keywords", nargs=-1)
def rbdd(keywords):
    """
    Run story with name containing keywords and rewrite.
    """
    _storybook(python_path=_devenv().python_path, rewrite=True).shortcut(
        *keywords
    ).play()


@cli.command()
@argument("keywords", nargs=-1)
def bdd(keywords):
    """
    Run story with name containing keywords.
    """
    _storybook(python_path=_devenv().python_path).shortcut(*keywords).play()


@cli.command()
@argument("filename")
def regressfile(filename):
    """
    Run all stories in filename 'filename'.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, python_path=_devenv().python_path)
    ).in_filename(filename).ordered_by_name().play()


@cli.command()
def rewriteall():
    """
    Run all stories in rewrite mode.
    """
    StoryCollection(
        pathquery(DIR.key).ext("story"),
        Engine(DIR, python_path=_devenv().python_path, rewrite=True),
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def regression():
    """
    Continuos integration - lint and run all stories.
    """
    # toolkit.lint(exclude=["__init__.py"])
    StoryCollection(
        pathquery(DIR.key).ext("story"), Engine(DIR, python_path=_devenv().python_path)
    ).only_uninherited().ordered_by_name().play()


@cli.command()
def reformat():
    """
    Reformat using black and then relint.
    """
    toolkit.reformat()


@cli.command()
def lint():
    """
    Lint project code and hitch code.
    """
    toolkit.lint(exclude=["__init__.py"])


@cli.command()
@argument("test", required=False)
def deploy(test="test"):
    """
    Deploy to pypi as specified version.
    """
    testpypi = not (test == "live")
    toolkit.deploy(testpypi=testpypi)


@cli.command()
def draftdocs():
    """
    Build documentation.
    """
    toolkit.draft_docs(storybook=_storybook(python_path=_devenv().python_path))


@cli.command()
def publishdocs():
    """Publish pushed docs."""
    toolkit.publish(storybook=_storybook(python_path=_devenv().python_path))


@cli.command()
def build():
    _devenv()


@cli.command()
def cleandevenv():
    DIR.gen.joinpath("pyenv", "versions", "devvenv").remove()


@cli.command()
@argument("strategy_name", nargs=1)
def envirotest(strategy_name):
    """Run tests on package / python version combinations."""
    import envirotest
    import pyenv

    test_package = pyenv.PythonRequirements(
        [
            "prettystack=={}".format(_current_version()),
        ],
        test_repo=True,
    )

    test_package = pyenv.PythonProjectDirectory(DIR.project)

    prerequisites = [
        pyenv.PythonVersionDependentRequirement(
            package="markupsafe",
            lower_version="2.0.0",
            python_version_threshold="3.9",
            higher_version="2.1.2",
        ),
        pyenv.PythonRequirements(
            [
                "ensure",
            ]
        ),
    ]

    envirotest.run_test(
        pyenv.Pyenv(DIR.gen / "pyenv"),
        DIR.project.joinpath("pyproject.toml").text(),
        test_package,
        prerequisites,
        strategy_name,
        _storybook,
        lambda python_path: False,
    )


if __name__ == "__main__":
    cli()
