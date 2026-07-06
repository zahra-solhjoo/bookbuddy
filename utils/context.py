from __future__ import annotations

from pathlib import Path
from typing import IO


class FileManager:
    """
    Context Manager for safe file handling.
    """

    def __init__(self, filename: str, mode: str, encoding: str = "utf-8") -> None:
        self.filename = Path(filename)
        self.mode = mode
        self.encoding = encoding
        self.file: IO | None = None

    def __enter__(self) -> IO:

        self.file = open(
            self.filename,
            self.mode,
            encoding=self.encoding,
        )

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:

        if self.file:
            self.file.close()

        return False