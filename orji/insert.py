from pathlib import Path
import click
from .template import Template
from .exceptions import OrjiError
import orgmunge
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from .ical import ICal
from .vcf import VCF


@click.command()
@click.argument("jinjafile")
@click.argument("relative")
@click.argument("location")
@click.argument("insertion")
def insert(jinjafile, relative, location, insertion):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(location)
    template_text = Path(jinjafile).read_text()

    varname, insertion_type, insertion_file = insertion.split(":")
    template = Template(template_text, jinjafile)

    if insertion_type == "ical":
        output_text = template.render(**{varname: ICal(insertion_file)})
    elif insertion_type == "text":
        output_text = template.render(**{varname: Path(insertion_file).read_text()})
    elif insertion_type == "vcf":
        output_text = template.render(**{varname: VCF(insertion_file)})
    else:
        raise OrjiError(f"{insertion_type} not known")

    chunk_to_insert = orgmunge.Org(
        output_text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )

    write_note = lookup.load(loader)

    if relative == "above":
        write_note.insert_above(output_text)
    elif relative == "below":
        write_note.insert_below(output_text)
    elif relative == "under":
        write_note.insert_under(output_text)
    elif relative == "replace":
        for note in chunk_to_insert.root.children:
            if write_note._node.sibling is None:
                write_note._org.root.add_child(note)
            else:
                write_note._node.sibling.add_child(note)
                note.sibling = write_note._node.sibling
                note.demote()
        write_note.delete()
    else:
        raise NotImplementedError("f{relative} not implemented")
    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
