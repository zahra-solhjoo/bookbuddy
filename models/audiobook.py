from __future__ import annotations

from datetime import datetime
from typing import Any

from models.book import Book
from models.book_type import BookType


class AudioBook(Book):

    def __init__(
        self,
        title: str,
        author: str,
        genre: str,
        pages: int,
        duration: int,
        narrator: str,
        audio_format: str,
        date_added: datetime | None = None,
    ) -> None:

        super().__init__(
            title=title,
            author=author,
            genre=genre,
            pages=pages,
            date_added=date_added,
        )

        self.book_type = BookType.AUDIOBOOK

        self.duration = duration
        self.narrator = narrator
        self.audio_format = audio_format.upper()

    def to_dict(self) -> dict[str, Any]:

        data = self.base_dict()

        data.update(
            {
                "type": self.book_type.value,
                "duration": self.duration,
                "narrator": self.narrator,
                "audio_format": self.audio_format,
            }
        )

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AudioBook":

        obj = cls(
            title=data["title"],
            author=data["author"],
            genre=data["genre"],
            pages=data["pages"],
            duration=data["duration"],
            narrator=data["narrator"],
            audio_format=data["audio_format"],
            date_added=datetime.fromisoformat(data["date_added"]),
        )

        obj.update_progress(data.get("read_pages", 0))

        return obj

    def __str__(self) -> str:

        return (
            f"🎧 {self.title} | {self.author} | {self.genre}\n"
            f"Narrator: {self.narrator} | Duration: {self.duration} min\n"
            f"Format: {self.audio_format}\n"
            f"{self.progress}% ({self.read_pages}/{self.pages})"
        )