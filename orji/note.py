from slugify import slugify
from pathlib import Path
from orji.utils import random_5_digit_number
import re


class OrjiError(Exception):
    pass


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


class Body(TextChunk):
    def __init__(self, text, working_dir):
        # import web_pdb; web_pdb.set_trace()
        self.text = str(text) if text is not None else ""
        self._working_dir = working_dir

    @property
    def oneline(self):
        if "\n" not in self.text.strip():
            return self.text.strip()
        else:
            raise OrjiError(f"{self.text} is not one line")

    def tempfile(self):
        # import web_pdb;web_pdb.set_trace()
        filepath = Path(f"{self._working_dir}/{random_5_digit_number()}.txt")
        filepath.write_text(self.text)
        return filepath.absolute()

    @property
    def paragraphs(self):
        return [
            TextChunk(text) for text in self.text.split("\n\n") if text.strip() != ""
        ]


class Note:
    def __init__(self, node, working_dir):
        self._node = node
        self._working_dir = working_dir

    @property
    def name(self):
        return self._node.headline.title

    @property
    def indexlookup(self):
        indices = []
        node = self._node
        while True:
            # import web_pdb; web_pdb.set_trace()
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
        return Body(self._node.body, self._working_dir)

    @property
    def prop(self):
        return self._node.properties

    def from_indexlookup(self, indexlookup):
        split = [int(x) for x in indexlookup.split("/")]
        node = self._node

        for index in split:
            node = node.children[index]

        return Note(node, self._working_dir)

    def has(self, lookup):
        matching_notes = [n for n in self._node.children if n.headline.title == lookup]
        if len(matching_notes) == 0:
            return False
        elif len(matching_notes) > 1:
            raise OrjiError(
                f"More than one note found in {self.name} with name {lookup}"
            )
        else:
            return True

    def at(self, lookup):
        matching_notes = [n for n in self._node.children if n.headline.title == lookup]
        if len(matching_notes) == 0:
            raise OrjiError(f"No notes found in {self.name} with name {lookup}")
        elif len(matching_notes) > 1:
            raise OrjiError(
                f"More than one note found in {self.name} with name {lookup}"
            )
        else:
            return Note(matching_notes[0], working_dir=self._working_dir)

    def __iter__(self):
        for node in self._node.children:
            yield Note(node, working_dir=self._working_dir)
