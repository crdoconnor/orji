import click
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from pathlib import Path
import orgmunge


class Modification:
    pass


class NewTitle(Modification):
    def __init__(self, relative: tuple[int, ...], title):
        self.relative = relative
        self.title = title


class AddError(Modification):
    def __init__(self, relative: tuple[int, ...], error_title, error_text):
        self.relative = relative
        self.error_title = error_title
        self.error_text = error_text


def perform_calculation(calc_note, modifications):
    headline = calc_note.name
    body = calc_note.body.text

    if body.startswith("=") and "=" in headline:
        formula = body.lstrip("=")
        left_hand_side = headline.split("=")[0]

        try:
            actual_value = eval(formula)
            modifications.append(NewTitle((0,), actual_value))
            new_title = left_hand_side + "= " + str(actual_value)
            if new_title != calc_note.name:
                modifications.append(NewTitle((0,), new_title))
        except Exception as error:
            modifications.append(
                AddError((0,), type(error).__name__.strip(), str(error))
            )


@click.command()
@click.argument("relative")
def calculation(relative):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)

    modifications: Modification = []

    calc_note = lookup.load(loader)
    perform_calculation(calc_note, modifications)

    for modification in modifications:
        children = [
            node
            for node in calc_note._node.children
            if node.tags is None or "calcerror" not in node.tags
        ]

        if isinstance(modification, NewTitle):
            calc_note.set_name(modification.title)
            calc_note._node.children = children
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
            chunk_to_insert.sibling = calc_note._node
            calc_note._node.children = children
            chunk_to_insert.demote()
        else:
            raise NotImplementedError

    Path(lookup.filepath).write_text(str(calc_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()