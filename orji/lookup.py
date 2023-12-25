import orgmunge
from .note import Note
from pathlib import Path


class LookupItem:
    def __init__(self, item):
        self.index = int(item)


class Lookup:
    def __init__(self, text):
        self._text = text

        split = text.split("//")
        if len(split) == 1:
            self.filepath = split[0]
            self.ref = None
        elif len(split) == 2:
            self.filepath = split[0]
            self.ref = split[1]
            self.parsed_ref = [LookupItem(item) for item in split[1].split("/")]
        else:
            raise NotImplementedError

    @property
    def full(self):
        return True

    def load(self, temp_dir):
        org_text = Path(self.filepath).read_text()
        munge_parsed = orgmunge.Org(
            org_text,
            from_file=False,
            todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
        )
        current_note = Note(munge_parsed.root, temp_dir=temp_dir)
        for item in self.parsed_ref:
            current_note = current_note.children[item.index]
        return current_note
