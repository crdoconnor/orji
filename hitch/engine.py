from hitchstory import (
    StoryCollection,
    BaseEngine,
    exceptions,
    validate,
    no_stacktrace_for,
)
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from templex import Templex
from strictyaml import Optional, Str, Map, Int, Bool, Enum, load, MapPattern
from path import Path
import hitchpylibrarytoolkit
from hitchrunpy import (
    ExamplePythonCode,
    HitchRunPyException,
    ExpectedExceptionMessageWasDifferent,
)


CODE_TYPE = Map({"in python 2": Str(), "in python 3": Str()}) | Str()


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        files=GivenProperty(MapPattern(Str(), Str())),
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
            self.path.working.joinpath(filename).write_text(contents)

        if not self.path.profile.exists():
            self.path.profile.mkdir()

        self.pylibrary = hitchpylibrarytoolkit.PyLibraryBuild(
            "orji", self.path
        ).with_python_version("3.7.0")
        self.pylibrary.ensure_built()
        self.python = self.pylibrary.bin.python
        self.orji_bin = self.pylibrary.bin.orji

    @no_stacktrace_for(AssertionError)
    @validate(cmd=Str(), output=Str(), error=Bool())
    def orji(self, cmd, output, error=False):
        from shlex import split
        from templex import Templex

        command = self.orji_bin(*split(cmd)).in_dir(self.path.working)

        if error:
            command = command.ignore_errors()

        actual_output = command.output()

        try:
            Templex(actual_output).assert_match(output)
        except AssertionError:
            if self._rewrite:
                self.current_step.update(output=actual_output)
            else:
                raise

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
