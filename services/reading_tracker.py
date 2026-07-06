from __future__ import annotations

from datetime import datetime

from models.reading_log import ReadingLog
from models.book import Book
from services.library_service import LibraryService
from exceptions.errors import BookNotFoundError, InvalidLogError


class ReadingTracker:

    def __init__(self, library: LibraryService):
        self.library = library

    # ----------------------------
    # Log reading session
    # ----------------------------

    def log_reading(
        self,
        title: str,
        pages_read: int,
        notes: str = "",
        reading_date: datetime | None = None,
    ) -> ReadingLog:

        if pages_read <= 0:
            raise InvalidLogError("Pages must be greater than zero.")

        book = self.library.find_book(title)

        if not book:
            raise BookNotFoundError("Book not found.")

        remaining = book.pages - book.read_pages

        if pages_read > remaining:
            pages_read = remaining

        log = ReadingLog(
            pages_read=pages_read,
            notes=notes,
            reading_date=reading_date or datetime.now(),
        )

        book.add_reading_log(log)

        return log

    # ----------------------------
    # Get logs
    # ----------------------------

    def get_logs(self, title: str) -> list[ReadingLog]:

        book = self.library.get_book(title)

        return sorted(
            book.reading_logs,
            key=lambda x: x.reading_date,
        )

    # ----------------------------
    # Remove last log (safe fix)
    # ----------------------------

    def remove_last_log(self, title: str) -> None:

        book = self.library.get_book(title)

        if not book.reading_logs:
            raise InvalidLogError("No logs found.")

        last_log = book.reading_logs.pop()

        book.decrease_progress(last_log.pages_read)

    # ----------------------------
    # Stats
    # ----------------------------

    def total_pages_read(self) -> int:

        return sum(
            book.read_pages for book in self.library
        )

    def total_logs(self) -> int:

        return sum(
            len(book.reading_logs)
            for book in self.library
        )

    def completed_books(self) -> list[Book]:

        return [
            book
            for book in self.library
            if book.is_completed
        ]

    # ----------------------------
    # Full history
    # ----------------------------

    def reading_history(self) -> list[dict]:

        history = []

        for book in self.library:

            for log in book.reading_logs:

                history.append(
                    {
                        "book": book.title,
                        "author": book.author,
                        "pages": log.pages_read,
                        "notes": log.notes,
                        "date": log.reading_date,
                    }
                )

        return sorted(
            history,
            key=lambda x: x["date"],
        )