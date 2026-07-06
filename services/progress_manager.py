from __future__ import annotations

from services.library_service import LibraryService


class ProgressManager:
    """
    Calculates reading progress and statistics.
    """

    def __init__(self, library: LibraryService) -> None:
        self.library = library

    # ==========================================
    # Single Book Progress
    # ==========================================

    def book_progress(self, title: str) -> dict:

        book = self.library.get_book(title)

        return {
            "title": book.title,
            "author": book.author,
            "pages": book.pages,
            "read_pages": book.read_pages,
            "progress": book.progress,
            "completed": book.is_completed,
        }

    # ==========================================
    # Book Collections
    # ==========================================

    @property
    def completed_books(self):

        return [
            book
            for book in self.library
            if book.is_completed
        ]

    @property
    def unread_books(self):

        return [
            book
            for book in self.library
            if book.read_pages == 0
        ]

    @property
    def books_in_progress(self):

        return [
            book
            for book in self.library
            if 0 < book.progress < 100
        ]

    # ==========================================
    # Overall Progress
    # ==========================================

    def overall_progress(self) -> float:

        total_pages = sum(
            book.pages
            for book in self.library
        )

        if total_pages == 0:
            return 0.0

        total_read = sum(
            book.read_pages
            for book in self.library
        )

        return round(
            (total_read / total_pages) * 100,
            2,
        )

    # ==========================================
    # Statistics
    # ==========================================

    def statistics(self) -> dict:

        total_books = len(self.library)

        total_pages = sum(
            book.pages
            for book in self.library
        )

        read_pages = sum(
            book.read_pages
            for book in self.library
        )

        average_progress = 0.0

        if total_books:

            average_progress = round(
                sum(
                    book.progress
                    for book in self.library
                )
                / total_books,
                2,
            )

        return {

            "total_books": total_books,

            "completed_books": len(
                self.completed_books
            ),

            "in_progress": len(
                self.books_in_progress
            ),

            "unread": len(
                self.unread_books
            ),

            "total_pages": total_pages,

            "read_pages": read_pages,

            "overall_progress": self.overall_progress(),

            "average_progress": average_progress,

        }

    # ==========================================
    # Console Output
    # ==========================================

    def show_progress(self) -> None:

        if len(self.library) == 0:

            print("\nLibrary is empty.\n")

            return

        print("\n========== READING PROGRESS ==========\n")

        for book in self.library:

            print(
                f"{book.title:<30}"
                f"{book.read_pages}/{book.pages}"
                f" ({book.progress}%)"
            )

        print("\n--------------------------------------")

        print(
            f"Overall Progress : "
            f"{self.overall_progress()}%"
        )

        print("--------------------------------------\n")