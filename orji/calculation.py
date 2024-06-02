import click
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from pathlib import Path
import orgmunge


@click.command()
@click.argument("relative")
def calculation(relative):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(relative)
    write_note = lookup.load(loader)

    headline = write_note.name
    body = write_note.body.text

    if body.startswith("=") and "=" in headline:
        formula = body.lstrip("=")
        left_hand_side = headline.split("=")[0]

        try:
            actual_value = eval(formula)
            write_note.set_name(left_hand_side + "= " + str(actual_value))
        except Exception as error:
            chunk_to_insert = orgmunge.Org(
                f"* {type(error).__name__.strip()} :calcerror:\n{str(error)}",
                from_file=False,
                todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
            ).root.children[0]
            write_note._node.parent.add_child(chunk_to_insert)
            chunk_to_insert.sibling = write_note._node
            chunk_to_insert.demote()

    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
