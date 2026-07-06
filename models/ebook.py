from __future__ import annotations

from datetime import datetime
from typing import Any

from models.book import Book
from models.book_type import BookType


class EBook(Book):

    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        pages: int,
        file_size: float,
        file_format: str,
        date_added: datetime | None = None,
    ) -> None:

        super().__init__(
            title=title,
            author=author,
            genre=genre,
            pages=pages,
            date_added=date_added,
        )

        self.book_type = BookType.EBOOK

        self.file_size = file_size
        self.file_format = file_format.upper()

    def to_dict(self) -> dict[str, Any]:

        data = self.base_dict()

        data.update(
            {
                "type": self.book_type.value,
                "file_size": self.file_size,
                "file_format": self.file_format,
            }
        )

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EBook":

        obj = cls(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            pages=data["pages"],
            file_size=data["file_size"],
            file_format=data["file_format"],
            date_added=datetime.fromisoformat(data["date_added"]),
        )

        obj.update_progress(data.get("read_pages", 0))

        return obj

    def __str__(self) -> str:

        return (
            f"📖 {self.title} | {self.author} | {self.genre}\n"
            f"Format: {self.file_format} | Size: {self.file_size}MB\n"
            f"{self.progress}% ({self.read_pages}/{self.pages})"
        )