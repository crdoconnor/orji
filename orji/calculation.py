import click
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from pathlib import Path
import orgmunge
from copy import copy
import inspect
import importlib.machinery
import importlib.util  #


class Modification:
    pass


class NewTitle(Modification):
    def __init__(self, relative, title):
        self.relative = relative
        self.title = title


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


def perform_calculation(calc_note, modifications, variables, module_contents):
    headline = calc_note.name
    body = calc_note.body.text

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
                modifications.append(NewTitle(calc_note, actual_value))
                new_title = left_hand_side + "= " + str(actual_value)
                if new_title != calc_note.name:
                    modifications.append(NewTitle(calc_note, new_title))
            except Exception as error:
                modifications.append(
                    AddError(calc_note, type(error).__name__.strip(), str(error))
                )

        variables[underscore_slugify(left_hand_side)] = (
            float(actual_value) if actual_value is not None else None
        )


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

    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)

    modifications: Modification = []
    variables = {}

    calc_note = lookup.load(loader)

    children = calc_note.children
    children.reverse()

    for child in children:
        perform_calculation(child, modifications, variables, module_contents)

    perform_calculation(calc_note, modifications, variables, module_contents)

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

    Path(lookup.filepath).write_text(str(calc_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
