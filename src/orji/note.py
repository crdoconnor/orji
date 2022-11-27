from slugify import slugify


class Line:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text


class Body:
    def __init__(self, node):
        self.text = node.body

    @property
    def lines(self):
        return [Line(line_text) for line_text in self.text.split("\n")]

    def __str__(self):
        return self.text


class Note:
    def __init__(self, node):
        self._node = node

    @property
    def name(self):
        return self._node.heading

    @property
    def slug(self):
        return slugify(self._node.heading)

    @property
    def state(self):
        return self._node.todo

    @property
    def tags(self):
        return self._node.tags

    @property
    def body(self):
        return Body(self._node)

    @property
    def prop(self):
        return self._node.properties

    def at(self, lookup):
        matching_notes = [n for n in self._node.children if n.heading == lookup]
        if len(matching_notes) == 0:
            raise Exception(f"No notes found in {self.heading} with name {lookup}")
        elif len(matching_notes) > 1:
            raise Exception(
                f"More than one notes found in {self.heading} with name {lookup}"
            )
        else:
            return Note(matching_notes[0])

    def __iter__(self):
        for node in self._node.children:
            yield Note(node)
