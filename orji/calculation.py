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


@click.command()
@click.argument("relative")
def calculation(relative):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)

    modifications: Modification = []

    write_note = lookup.load(loader)

    headline = write_note.name
    body = write_note.body.text

    if body.startswith("=") and "=" in headline:
        formula = body.lstrip("=")
        left_hand_side = headline.split("=")[0]

        try:
            actual_value = eval(formula)
            modifications.append(NewTitle((0,), actual_value))
            new_title = left_hand_side + "= " + str(actual_value)
            if new_title != write_note.name:
                modifications.append(NewTitle((0,), new_title))
        except Exception as error:
            modifications.append(
                AddError((0,), type(error).__name__.strip(), str(error))
            )

    for modification in modifications:
        children = [
            node
            for node in write_note._node.children
            if node.tags is None or "calcerror" not in node.tags
        ]

        if isinstance(modification, NewTitle):
            write_note.set_name(new_title)
            write_note._node.children = children
        elif isinstance(modification, AddError):
            chunk_to_insert = orgmunge.Org(
                f"* {modification.error_title} :calcerror:\n{modification.error_text}",
                from_file=False,
                todos={
                    "todo_states": {"todo": "TODO"},
                    "done_states": {"done": "DONE"},
                },
            ).root.children[0]
            write_note._node.parent.add_child(chunk_to_insert)
            chunk_to_insert.sibling = write_note._node
            chunk_to_insert.demote()
        else:
            raise NotImplementedError

    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
