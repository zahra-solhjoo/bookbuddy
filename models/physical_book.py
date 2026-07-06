from __future__ import annotations

from datetime import datetime
from typing import Any

from models.book import Book
from models.book_type import BookType


class PhysicalBook(Book):

    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        pages: int,
        publisher: str = "",
        shelf: str = "",
        date_added: datetime | None = None,
    ) -> None:

        super().__init__(
            title=title,
            author=author,
            genre=genre,
            pages=pages,
            date_added=date_added,
        )

        self.book_type = BookType.PHYSICAL
        self.publisher = publisher
        self.shelf = shelf

    def to_dict(self) -> dict[str, Any]:

        data = self.base_dict()

        data.update(
            {
                "type": self.book_type.value,
                "publisher": self.publisher,
                "shelf": self.shelf,
            }
        )

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PhysicalBook":

        obj = cls(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            pages=data["pages"],
            publisher=data.get("publisher", ""),
            shelf=data.get("shelf", ""),
            date_added=datetime.fromisoformat(data["date_added"]),
        )

        obj.update_progress(data.get("read_pages", 0))

        return obj

    def __str__(self) -> str:

        return (
            f"📘 {self.title} | {self.author} | {self.genre}\n"
            f"Publisher: {self.publisher} | Shelf: {self.shelf}\n"
            f"{self.progress}% ({self.read_pages}/{self.pages})"
        )