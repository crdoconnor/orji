from pathlib import Path
from .note import Note, NoteGroup
from .exceptions import OrjiError
import orgmunge


class Loader:
    def __init__(self, temp_dir, multiple_files_ok=False):
        self._temp_dir = temp_dir
        self._multiple_files_ok = multiple_files_ok

    def load(self, filepath: str):
        filepath_obj = Path(filepath)
        if filepath_obj.is_dir():
            if self._multiple_files_ok:
                notes = []
                for orgfile in filepath_obj.glob("*.org"):
                    org_text = orgfile.read_text()
                    munge_parsed = orgmunge.Org(
                        org_text,
                        from_file=False,
                        todos={
                            "todo_states": {"todo": "TODO"},
                            "done_states": {"done": "DONE"},
                        },
                    )
                    notes.append(Note(munge_parsed.root, loader=self, org=munge_parsed))
                return NoteGroup(notes)
            else:
                raise OrjiError(f"{filepath} is a directory.")
        else:
            org_text = Path(filepath).read_text()
            munge_parsed = orgmunge.Org(
                org_text,
                from_file=False,
                todos={
                    "todo_states": {"todo": "TODO"},
                    "done_states": {"done": "DONE"},
                },
            )
            return Note(munge_parsed.root, loader=self, org=munge_parsed)
