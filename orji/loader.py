from pathlib import Path
from .note import Note
import orgmunge


class Loader:
    def __init__(self, temp_dir):
        self._temp_dir = temp_dir

    def load(self, filepath):
        org_text = Path(filepath).read_text()
        munge_parsed = orgmunge.Org(
            org_text,
            from_file=False,
            todos={"todo_states": {"todo": "TODO"}, "done_states": {"done": "DONE"}},
        )
        return Note(munge_parsed.root, loader=self)
