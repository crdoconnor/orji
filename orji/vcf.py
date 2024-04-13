import vobject
import jinja2
from pathlib import Path
from vobject.base import Component

DEFAULT = jinja2.Template(
    """\
{% for contact in contacts %}* {{ contact.fullname }}

tel:{{ contact.tel }}
{% endfor %}"""
)


class VCard:
    def __init__(self, vcard: Component):
        self._vcard = vcard

    @property
    def name(self):
        return self._vcard.n.value

    @property
    def fullname(self):
        return "".join(
            [
                (namepart + " ").lstrip()
                for namepart in (
                    self.name.prefix,
                    self.name.given,
                    self.name.family,
                    self.name.suffix,
                    self.name.additional,
                )
            ]
        )

    @property
    def tel(self):
        return self._vcard.tel.value


class VCF:
    def __init__(self, filename):
        self._vcftext = Path(filename).read_text()
        self._vcf = [VCard(vobj) for vobj in vobject.readComponents(self._vcftext)]

    def to_org(self):
        return DEFAULT.render(contacts=self._vcf)
