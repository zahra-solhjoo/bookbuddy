from __future__ import annotations

from models.physical_book import PhysicalBook
from models.ebook import EBook
from models.audiobook import AudioBook
from models.book_type import BookType
from models.book import Book


class BookFactory:

    @staticmethod
    def create(data: dict) -> Book :

        book_type = data.get("type")

        if book_type == BookType.PHYSICAL.value:
            return PhysicalBook.from_dict(data)

        if book_type == BookType.EBOOK.value:
            return EBook.from_dict(data)

        if book_type == BookType.AUDIOBOOK.value:
            return AudioBook.from_dict(data)

        raise ValueError(f"Unknown book type: {book_type}")