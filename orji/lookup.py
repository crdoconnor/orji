from enum import Enum
from .exceptions import OrjiError


class LookupType(Enum):
    FILE = 0
    ABSOLUTE = 1
    RELATIVE = 2
    FILEONLY = 3


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
    def __init__(self, text, relative_to=None):
        self.relative_to = relative_to

        if "//" in text:
            self.lookup_type = LookupType.FILE
            split = text.split("//")
            self.filepath = split[0]
            self.ref = split[1]
            self.parsed_ref = [LookupItem(item) for item in self.ref.split("/")]
        elif text.startswith("./"):
            self.lookup_type = LookupType.RELATIVE
            raise NotImplementedError
        elif text.startswith("/"):
            self.lookup_type = LookupType.ABSOLUTE
            raise NotImplementedError
        else:
            if relative_to is None:
                self.lookup_type = LookupType.FILEONLY
                self.filepath = text
                self.parsed_ref = []
                self.ref = None
            else:
                self.lookup_type = LookupType.RELATIVE
                self.ref = text
                self.parsed_ref = [LookupItem(item) for item in text.split("/")]

    def exists(self, loader):
        return self.load(loader, fail_if_nonexistent=False) is not None

    def load(self, loader, fail_if_nonexistent=True):
        if self.relative_to is None:
            current_note = loader.load(self.filepath)
        else:
            current_note = self.relative_to
        for item in self.parsed_ref:
            if item.item_type == LookupItemType.INDEX:
                current_note = current_note.children[item.index]
            else:
                matching_notes = [
                    note for note in current_note.children if note.name == item.name
                ]
                if len(matching_notes) == 1:
                    return matching_notes[0]
                elif len(matching_notes) > 1:
                    raise OrjiError(f"More than one note found matching '{self.ref}'")
                else:
                    if fail_if_nonexistent:
                        raise OrjiError(f"No notes matching '{self.ref}' found.")
                    else:
                        return None
        return current_note
