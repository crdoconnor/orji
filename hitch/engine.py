from hitchstory import (
    StoryCollection,
    BaseEngine,
    exceptions,
    validate,
    no_stacktrace_for,
    strings_match,
    Failure,
)
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from templex import Templex
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern, EmptyDict
from path import Path
import hitchpylibrarytoolkit
from hitchrunpy import (
    ExamplePythonCode,
    HitchRunPyException,
    ExpectedExceptionMessageWasDifferent,
)
from shlex import split
from templex import Templex
from commandlib import Command


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        files=GivenProperty(
            MapPattern(Str(), Str()),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    info_definition = InfoDefinition(
        status=InfoProperty(schema=Enum(["experimental", "stable"])),
        docs=InfoProperty(schema=Str()),
    )

    def __init__(self, keypath, python_path=None, rewrite=False, cprofile=False):
        self.path = keypath
        self._python_path = python_path
        self._rewrite = rewrite
        self._cprofile = cprofile

    def set_up(self):
        """Set up your applications and the test environment."""
        self.path.profile = self.path.gen.joinpath("profile")
        self.path.working = self.path.gen.joinpath("working")

        if self.path.working.exists():
            self.path.working.rmtree()
        self.path.working.mkdir()

        for filename, contents in self.given["files"].items():
            filepath = self.path.working.joinpath(filename)
            if not filepath.dirname().exists():
                filepath.dirname().mkdir()
            self.path.working.joinpath(filename).write_text(contents)

        if not self.path.profile.exists():
            self.path.profile.mkdir()

        self.python = Command(self._python_path)
        self.orji_bin = Command(self._python_path.parent / "orji").with_env(MOCK="yes")

    @no_stacktrace_for(AssertionError)
    @validate(
        cmd=Str(),
        output=Str(),
        env=MapPattern(Str(), Str()) | EmptyDict(),
        error=Bool(),
    )
    def orji(self, cmd, output, env=None, error=False):
        env = {} if env is None else env
        command = self.orji_bin(*split(cmd)).with_env(**env).in_dir(self.path.working)

        if error:
            command = command.ignore_errors()

        actual_output = command.output()

        try:
            strings_match(output, actual_output)
        except Failure:
            if self._rewrite:
                self.current_step.update(output=actual_output)
            else:
                raise

    @no_stacktrace_for(AssertionError)
    def pdf(self, cmd):
        output = self.orji_bin(*split(cmd)).in_dir(self.path.working).output()
        self.path.working.joinpath("latex.tex").write_text(output)
        from commandlib import Command

        self.path.working.chdir()
        # import IPython ; IPython.embed()
        Command("pdflatex", "latex.tex").in_dir(self.path.working).run()

    def pause(self, message="Pause"):
        import IPython

        IPython.embed()

    def on_success(self):
        if self._rewrite:
            self.new_story.save()
        if self._cprofile:
            self.python(
                self.path.key.joinpath("printstats.py"),
                self.path.profile.joinpath("{0}.dat".format(self.story.slug)),
            ).run()
