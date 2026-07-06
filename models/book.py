from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from models.reading_log import ReadingLog


class Book(ABC):
    """
    Abstract base class for all book types.
    """

    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        pages: int,
        date_added: datetime | None = None,
    ) -> None:

        if not self.validate_book_data(title, author, pages):
            raise ValueError("Invalid book information.")

        self.title = title.strip()
        self.author = author.strip()
        self.genre = genre.strip()
        self.pages = pages

        self.date_added = date_added or datetime.now()

        self._read_pages = 0

        self.reading_logs: list[ReadingLog] = []

    # =====================================
    # Properties
    # =====================================

    @property
    def read_pages(self) -> int:
        return self._read_pages

    @property
    def progress(self) -> float:

        if self.pages == 0:
            return 0.0

        return round(
            (self._read_pages / self.pages) * 100,
            2,
        )

    @property
    def is_completed(self) -> bool:
        return self._read_pages >= self.pages

    # =====================================
    # Reading Progress
    # =====================================

    def update_progress(self, pages: int) -> None:

        if pages <= 0:
            raise ValueError(
                "Pages must be greater than zero."
            )

        self._read_pages += pages

        if self._read_pages > self.pages:
            self._read_pages = self.pages

    def decrease_progress(self, pages: int) -> None:

        if pages <= 0:
            return

        self._read_pages -= pages

        if self._read_pages < 0:
            self._read_pages = 0

    def add_reading_log(
        self,
        log: ReadingLog,
    ) -> None:

        self.reading_logs.append(log)

        self.update_progress(log.pages_read)

    # =====================================
    # Common Dictionary
    # =====================================

    def base_dict(self) -> dict[str, Any]:

        return {

            "title": self.title,

            "author": self.author,

            "genre": self.genre,

            "pages": self.pages,

            "date_added": self.date_added.isoformat(),

            "read_pages": self._read_pages,

        }

    # =====================================
    # Validation
    # =====================================

    @staticmethod
    def validate_book_data(
        title: str,
        author: str,
        pages: int,
    ) -> bool:

        return (

            bool(title.strip())

            and bool(author.strip())

            and pages > 0

        )

    # =====================================
    # Abstract Methods
    # =====================================

    @abstractmethod
    def to_dict(self) -> dict[str, Any]:
        """
        Convert object to dictionary.
        """
        pass

    @classmethod
    @abstractmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ):
        """
        Create object from dictionary.
        """
        pass

    # =====================================
    # Magic Methods
    # =====================================

    def __str__(self) -> str:

        return (
            f"{self.title} | "
            f"{self.author} | "
            f"{self.read_pages}/{self.pages} "
            f"({self.progress}%)"
        )

    def __repr__(self) -> str:

        return (
            f"{self.__class__.__name__}("
            f"title='{self.title}', "
            f"author='{self.author}')"
        )