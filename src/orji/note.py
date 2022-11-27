from slugify import slugify


class Body:
    def __init__(self, text):
        self.text = text
    
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
    def body(self):
        return Body(self._node.body)

    def __iter__(self):
        for node in self._node.children:
            yield Note(node)
