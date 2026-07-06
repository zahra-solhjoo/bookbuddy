from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class ReadingLog:

    pages_read: int
    notes: str = ""
    reading_date: datetime = field(default_factory=datetime.now)

    def __post_init__(self):

        if self.pages_read <= 0:
            raise ValueError("Pages read must be greater than zero.")

    def to_dict(self) -> dict[str, Any]:

        return {

            "pages_read": self.pages_read,

            "notes": self.notes,

            "reading_date": self.reading_date.isoformat(),

        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ReadingLog":

        return cls(

            pages_read=data["pages_read"],

            notes=data.get("notes", ""),

            reading_date=datetime.fromisoformat(
                data["reading_date"]
            ),

        )

    def __str__(self) -> str:

        return (
            f"{self.reading_date.strftime('%Y-%m-%d %H:%M')} | "
            f"{self.pages_read} pages | "
            f"{self.notes}"
        )

    @property
    def has_notes(self):

        return bool(self.notes.strip())        