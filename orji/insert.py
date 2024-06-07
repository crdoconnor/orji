from pathlib import Path
import click
from .template import Template
from .exceptions import OrjiError
from .tempdir import TempDir
from .loader import Loader
from .lookup import Lookup
from .ical import ICal
from .vcf import VCF


@click.command()
@click.argument("jinjafile")
@click.argument("relative")
@click.argument("location")
@click.argument("insertions", nargs=-1)
def insert(jinjafile, relative, location, insertions):
    temp_dir = TempDir()
    temp_dir.create()
    loader = Loader(temp_dir)
    lookup = Lookup(location)
    template_text = Path(jinjafile).read_text()

    variables = {}

    for insertion in insertions:
        varname, insertion_type, insertion_reference = insertion.split(":")
        template = Template(template_text, jinjafile)

        if insertion_type == "ical":
            variables[varname] = ICal(insertion_reference)
        elif insertion_type == "text":
            variables[varname] = Path(insertion_reference).read_text()
        elif insertion_type == "vcf":
            variables[varname] = VCF(insertion_reference)
        elif insertion_type == "snippet":
            variables[varname] = insertion_reference
        else:
            raise OrjiError(f"{insertion_type} not known")

    output_text = template.render(**variables)

    write_note = lookup.load(loader)

    if relative == "above":
        write_note.insert_above(output_text)
    elif relative == "below":
        write_note.insert_below(output_text)
    elif relative == "under":
        write_note.insert_under(output_text)
    elif relative == "replace":
        write_note.replace(output_text)
    else:
        raise NotImplementedError("f{relative} not implemented")
    Path(lookup.filepath).write_text(str(write_note))
    click.echo("Written note(s) successfully")
    temp_dir.destroy()
