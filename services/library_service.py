from __future__ import annotations

from typing import Generic, TypeVar, Iterator

from models.book import Book
from exceptions.errors import BookNotFoundError, DuplicateBookError


T = TypeVar("T", bound=Book)


class LibraryService(Generic[T]):

    def __init__(self) -> None:
        self._books: list[T] = []

    # ----------------------------
    # Add Book
    # ----------------------------

    def add_book(self, book: T) -> None:

        if self.find_book(book.title):
            raise DuplicateBookError("Book already exists.")

        self._books.append(book)

    # ----------------------------
    # Remove Book
    # ----------------------------

    def remove_book(self, title: str) -> None:

        book = self.get_book(title)
        self._books.remove(book)

    # ----------------------------
    # Get Book (strict)
    # ----------------------------

    def get_book(self, title: str) -> T:

        for book in self._books:

            if book.title.lower() == title.lower():
                return book

        raise BookNotFoundError("Book not found.")

    # ----------------------------
    # Find Book (safe)
    # ----------------------------

    def find_book(self, title: str) -> T | None:

        for book in self._books:

            if book.title.lower() == title.lower():
                return book

        return None

    # ----------------------------
    # Search
    # ----------------------------

    def search(self, keyword: str) -> list[T]:

        keyword = keyword.lower()

        return [

            book

            for book in self._books

            if keyword in book.title.lower()

            or keyword in book.author.lower()

            or keyword in book.genre.lower()

        ]

    # ----------------------------
    # List
    # ----------------------------

    def list_books(self) -> list[T]:

        return self._books.copy()

    # ----------------------------
    # Stats
    # ----------------------------

    def total_books(self) -> int:

        return len(self._books)

    def completed_books(self) -> int:

        return sum(

            1 for b in self._books if b.is_completed

        )

    def total_pages(self) -> int:

        return sum(

            b.pages for b in self._books

        )

    # ----------------------------
    # Clear
    # ----------------------------

    def clear(self) -> None:

        self._books.clear()

    # ----------------------------
    # Iterator support
    # ----------------------------

    def __iter__(self) -> Iterator[T]:

        return iter(self._books)

    def __len__(self) -> int:

        return len(self._books)

    def __contains__(self, title: str) -> bool:

        return self.find_book(title) is not None

    def is_empty(self) -> bool:
        return len(self._books) == 0    