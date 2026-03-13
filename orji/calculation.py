import click
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from pathlib import Path
import orgmunge
from copy import copy
import inspect
import importlib.machinery
import importlib.util
from dataclasses import dataclass
from datetime import datetime
from orgmunge.classes import Scheduling, TimeStamp
from orgmunge import Headline, Heading
from datetime import datetime

class Modification:
    pass


class NewChildren(Modification):
    def __init__(self, relative, new_children):
        self.relative = relative
        self.new_children = new_children

class NewTitle(Modification):
    def __init__(self, relative, title):
        self.relative = relative
        self.title = title


class NewDatetime(Modification):
    def __init__(self, relative, new_datetime):
        self.relative = relative
        self.new_datetime = new_datetime


class AddError(Modification):
    def __init__(self, relative, error_title, error_text):
        self.relative = relative
        self.error_title = error_title
        self.error_text = error_text


def slugify(text, separator="-"):
    return text.lower().strip().replace(" ", separator)


def underscore_slugify(text):
    """Changes "Something like this" to "something_like_this"."""
    return slugify(text, separator="_")

@dataclass
class CalcNote:
    sched_start: datetime | None = None
    sched_end: datetime | None = None

    @property
    def sched(self):
        return self.sched_start


def perform_calculation(calc_note, modifications, variables, module_contents):
    headline = calc_note.name
    body = calc_note.body.text

    if headline.endswith(">"):
        if body.startswith("="):
            formula = body.lstrip("=")
            injected = copy(module_contents)
            injected.update(copy(variables))
            actual_list = eval(formula, injected)

            try:
                modifications.append(NewChildren(calc_note, actual_list))
            except Exception as error:
                modifications.append(
                    AddError(calc_note, type(error).__name__.strip(), str(error))
                )


    if "=" in headline:
        left_hand_side = headline.split("=")[0]

        try:
            actual_value = float(headline.split("=")[1])
        except ValueError:
            actual_value = None

        if body.startswith("="):
            formula = body.lstrip("=")

            injected = copy(module_contents)
            injected.update(copy(variables))

            try:
                actual_value = eval(formula, injected)
                new_title = left_hand_side + "= " + str(actual_value)
                if new_title != calc_note.name:
                    modifications.append(NewTitle(calc_note, new_title))
            except Exception as error:
                modifications.append(
                    AddError(calc_note, type(error).__name__.strip(), str(error))
                )

        if body.startswith("sched ="):
            formula = body.lstrip("sched").lstrip().lstrip("=").lstrip()

            injected = copy(module_contents)
            injected.update(copy(variables))

            try:
                new_datetime = eval(formula, injected)
                if calc_note._node.scheduling is None:
                    modifications.append(NewDatetime(calc_note, new_datetime))
                else:
                    if new_datetime != calc_note._node.scheduling.SCHEDULED.start_time:
                        modifications.append(NewDatetime(calc_note, new_datetime))
            except Exception as error:
                modifications.append(
                    AddError(calc_note, type(error).__name__.strip(), str(error))
                )

        variables[underscore_slugify(left_hand_side)] = actual_value

    if calc_note._node.scheduling is not None:
        if calc_note._node.scheduling.SCHEDULED is not None:
            start_time = calc_note._node.scheduling.SCHEDULED.start_time
            variables[underscore_slugify(headline)] = CalcNote(
                sched_start=calc_note._node.scheduling.SCHEDULED.start_time,
                sched_end=calc_note._node.scheduling.SCHEDULED.end_time
            )

    if len(calc_note._node.tags) > 0 and "calctext" in calc_note._node.tags:
        variables[underscore_slugify(headline)] = calc_note.body.text


@click.command()
@click.argument("relative")
@click.option(
    "--module",
    "pymodule",
    help="Specify python module to use in calculations.",
)
def calculation(relative, pymodule):
    if pymodule is not None:
        pymodule_filepath = Path(pymodule)

        if not pymodule_filepath.exists():
            click.echo(f"{pymodule} not found", err=True)
            exit(1)

        loader = importlib.machinery.SourceFileLoader(
            pymodule_filepath.stem, str(pymodule_filepath.absolute())
        )
        spec = importlib.util.spec_from_loader(loader.name, loader)
        imported_pymodule = importlib.util.module_from_spec(spec)
        loader.exec_module(imported_pymodule)

        module_contents = {
            key: item
            for key, item in inspect.getmembers(imported_pymodule)
            if not key.startswith("_")
        }
    else:
        module_contents = {}

    @dataclass
    class CalcNote:
        state: str
        title: str
        scheduled: datetime
        body: str | None

    module_contents["CalcNote"] = CalcNote

    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)

    modifications: Modification = []
    variables = {}

    calc_notes = lookup.load(loader)

    for calc_note in calc_notes:
        if calc_note.state != "DONE":
            perform_calculation(calc_note, modifications, variables, module_contents)

            if "subcalc" in calc_note.tags:
                for subcalc_note in calc_note.children:
                    perform_calculation(subcalc_note, modifications, variables, module_contents)

    for modification in modifications:
        modify_note = modification.relative
        children = [
            node
            for node in modify_note._node.children
            if node.tags is None or "calcerror" not in node.tags
        ]

        if isinstance(modification, NewTitle):
            modify_note.set_name(modification.title)
            modify_note._node.children = children
        elif isinstance(modification, NewDatetime):
            modify_note._node.scheduling = Scheduling(keyword="scheduled", timestamp=TimeStamp(modification.new_datetime.strftime("<%Y-%m-%d %a>")))
            modify_note._node.children = children
        elif isinstance(modification, NewChildren):
            heading_level = "*" * (modify_note._node.headline.level + 1)
            todos = modify_note._org.todos
            modify_note._node.children = [
                Heading(
                    headline=Headline(
                        level=heading_level,
                        title=child.title,
                        todos=todos,
                        todo=child.state,
                    ),
                    contents=(
                        Scheduling(keyword="scheduled", timestamp=TimeStamp(child.scheduled.strftime("<%Y-%m-%d %a>"))),
                        None,
                        child.body
                    ),
                ) for child in modification.new_children
            ]
        elif isinstance(modification, AddError):
            chunk_to_insert = orgmunge.Org(
                f"* {modification.error_title} :calcerror:\n{modification.error_text}",
                from_file=False,
                todos={
                    "todo_states": {"todo": "TODO"},
                    "done_states": {"done": "DONE"},
                },
            ).root.children[0]
            children = list(children)
            chunk_to_insert.sibling = modify_note._node
            modify_note._node.children = children
            chunk_to_insert.demote()
        else:
            raise NotImplementedError

    Path(lookup.filepath).write_text(str(calc_notes))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
