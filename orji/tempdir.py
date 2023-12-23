import os
from .utils import random_5_digit_number
from pathlib import Path
import shutil


class TempDir:
    """
    Handle temporary directory and files
    """

    def __init__(self):
        self._root = Path(os.getenv("ORJITMP", "."))

    def create(self):
        assert self._root.exists()
        assert self._root.is_dir()
        self.working_dir = self._root / f"{random_5_digit_number()}.tmp"
        self.working_dir.mkdir()

    def tempfile(self, text, filename=None):
        if filename is None:
            filename = f"{random_5_digit_number()}.txt"
        filepath = Path(f"{self.working_dir}/{filename}").absolute()
        filepath.write_text(text)
        return filepath

    def destroy(self):
        shutil.rmtree(self.working_dir.absolute())
