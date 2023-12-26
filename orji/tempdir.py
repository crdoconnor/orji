import os
from pathlib import Path
import shutil
import random

MOCK_RANDOM_FIX = 11110


def random_5_digit_number():
    if os.getenv("MOCK") == "yes":
        global MOCK_RANDOM_FIX
        MOCK_RANDOM_FIX = MOCK_RANDOM_FIX + 1
        return MOCK_RANDOM_FIX
    else:
        return random.randint(10000, 99999)


class TempDir:
    """
    Handle temporary directory and files
    """

    def __init__(self):
        self.orjitmp = Path(os.getenv("ORJITMP", "."))

    def create(self):
        assert self.orjitmp.exists()
        assert self.orjitmp.is_dir()
        self.working_dir = self.orjitmp.joinpath(
            f"{random_5_digit_number()}.tmp"
        ).absolute()
        self.working_dir.mkdir()

    def tempfile(self, text, filename=None):
        if filename is None:
            filename = f"{random_5_digit_number()}.txt"
        filepath = Path(f"{self.working_dir}/{filename}").absolute()
        filepath.write_text(text)
        return filepath

    def destroy(self):
        shutil.rmtree(self.working_dir.absolute())
