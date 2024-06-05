from slugify import slugify
from .exceptions import OrjiError
from .lookup import Lookup
import orgmunge
import re


class NoteGroup:
    def __init__(self, notes):
        self._notes = notes

    def walk(self):
        all_notes = [note.walk() for note in self._notes]
        return [subnote for note in all_notes for subnote in note]


class TextChunk:
    def __init__(self, text):
        self.text = str(text) if text is not None else ""

    @property
    def markdown(self):
        text = self.text
        text = re.sub(
            re.compile(r"\[\[(.*?)\]\[(.*?)\]\]"),
            r"[\2](\1)",
            text,
        )
        text = text.replace("\n+ ", "\n* ")
        return text.strip()

    @property
    def latexed(self):
        text = self.text
        text = re.sub(
            re.compile(r"\[\[(.*?)\]\[(.*?)\]\]"),
            r"\\href{\1}{\2}",
            text,
        )
        text = text.replace("&", "\\&")
        return text.strip()

    @property
    def strip(self):
        return self.text.strip()

    def __str__(self):
        return self.text.strip()


class Links:
    def __init__(self, note):
        self._note = note

    def _grab(self, link_type, link_name):
        matching = list(
            re.findall(link_type + r"\:(.*)?(?:\s|$)", self._note.body.text)
        )
        if len(matching) == 0:
            raise OrjiError(f"No {link_name} detected")
        elif len(matching) > 1:
            raise OrjiError(f"Over one ({len(matching)}) {link_name} detected")
        else:
            return matching[0]

    @property
    def tel(self):
        return self._grab(r"tel", "telephone numbers")

    @property
    def sms(self):
        return self._grab(r"sms", "SMS numbers")

    @property
    def file(self):
        return self._grab(r"file", "file (file:) links")

    @property
    def mailto(self):
        return self._grab(r"mailto", "mailto (mailto:) links")


class Body(TextChunk):
    def __init__(self, text, temp_dir):
        self.text = str(text) if text is not None else ""
        self._temp_dir = temp_dir

    @property
    def oneline(self):
        if "\n" not in self.text.strip():
            return self.text.strip()
        else:
            raise OrjiError(f"{self.text} is not one line")

    def tempfile(self):
        return self._temp_dir.tempfile(self.text)

    @property
    def paragraphs(self):
        return [
            TextChunk(text) for text in self.text.split("\n\n") if text.strip() != ""
        ]


def parsed(text):
    return orgmunge.Org(
        text,
        from_file=False,
        todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
    )


class Note:
    def __init__(self, node, loader, org):
        self._node = node
        self._loader = loader
        self._org = org

    @property
    def name(self):
        return self._node.headline.title

    def set_name(self, new_name):
        self._node.headline.title = new_name

    @property
    def links(self):
        return Links(self)

    @property
    def indexlookup(self):
        indices = []
        node = self._node
        while True:
            index = [i for i, n in enumerate(node.parent.children) if n == node][0]
            indices.append(str(index))
            if node.parent.parent is None:
                break
            else:
                node = node.parent

        return "/".join(reversed(indices))

    @property
    def slug(self):
        return slugify(self._node.headline.title)

    @property
    def state(self):
        return self._node.todo

    @property
    def tags(self):
        unsorted = self._node.tags
        return sorted(unsorted) if unsorted is not None else []

    @property
    def body(self):
        return Body(self._node.body, self._loader._temp_dir)

    @property
    def prop(self):
        return self._node.properties

    def from_indexlookup(self, indexlookup):
        split = [int(x) for x in indexlookup.split("/")]
        node = self._node

        for index in split:
            node = node.children[index]

        return Note(node, self._loader, self._rg)

    def delete(self):
        parent = self._node.parent
        node_index = [
            i for i, node in enumerate(parent.children) if node == self._node
        ][0]
        del parent.children[node_index]

    def delete_children(self):
        self._node.children = []

    def has(self, lookup):
        return Lookup(lookup, relative_to=self).exists(loader=self._loader)

    def at(self, lookup):
        return Lookup(lookup, relative_to=self).load(loader=self._loader)

    def __str__(self):
        return str(self._org)

    def _walk_iter(self, node):
        if len(node.children) == 0:
            return [Note(node, self._loader, self._org)]
        children = []
        for child in node.children:
            children.extend(self._walk_iter(child))
        return children

    def walk(self):
        return self._walk_iter(self._node)

    @property
    def children(self):
        return [Note(node, self._loader, self._org) for node in self._node.children]

    def insert_above(self, text):
        for note in parsed(text).root.children:
            if self._node.sibling is None:
                self._org.root.add_child(note)
            else:
                self._node.sibling.add_child(note)
                note.sibling = self._node.sibling
                note.demote()

    def insert_below(self, text):
        for note in parsed(text).root.children:
            self._node.add_child(note)

            for _ in range(self._node.level - 1):
                note.sibling = self._node
                note.demote()

    def insert_under(self, text):
        node_to_insert_under = self._node
        for note in parsed(text).root.children:
            node_to_insert_under.parent.add_child(note)

            for _ in range(self._node.level):
                note.sibling = self._node
                note.demote()

            node_to_insert_under = note

    def __iter__(self):
        for node in self._node.children:
            yield Note(node, self._loader, self._org)
