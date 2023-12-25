import orgmunge
from .note import Note
from pathlib import Path
from enum import Enum


class LookupItemType(Enum):
    INDEX = 0
    NAME = 1


class LookupItem:
    def __init__(self, item: str):
        if item.isdigit():
            self.item_type = LookupItemType.INDEX
            self.index = int(item)
        elif item.startswith("'") and item.endswith("'"):
            self.name = item.strip("'")
            self.item_type = LookupItemType.NAME
        else:
            self.item_type = LookupItemType.NAME
            self.name = item


class Lookup:
    def __init__(self, text):
        self._text = text

        split = text.split("//")
        if len(split) == 1:
            self.filepath = split[0]
            self.ref = None
            self.parsed_ref = []
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
            if item.item_type == LookupItemType.INDEX:
                current_note = current_note.children[item.index]
            else:
                matching_notes = [
                    note for note in current_note.children if note.name == item.name
                ]
                if len(matching_notes) == 1:
                    return matching_notes[0]
                else:
                    raise NotImplementedError
        return current_note
