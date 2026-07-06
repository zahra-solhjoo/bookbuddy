from __future__ import annotations

from colorama import Fore, Style, init

from config.logger import logger

from exceptions.errors import (
    BookBuddyError,
)

from models.physical_book import PhysicalBook
from models.ebook import EBook
from models.audiobook import AudioBook

from services.library_service import LibraryService
from services.reading_tracker import ReadingTracker
from services.progress_manager import ProgressManager

from storage.data_exporter import DataExporter

# Initialize Colorama
init(autoreset=True)


class BookBuddyCLI:
    """
    Command Line Interface for BookBuddy.
    """

    def __init__(self) -> None:

        self.library = LibraryService()

        self.tracker = ReadingTracker(
            self.library
        )

        self.progress = ProgressManager(
            self.library
        )

        self.running = True

        logger.info("BookBuddy started.")

    # ==========================================
    # Helper Methods
    # ==========================================

    @staticmethod
    def title() -> None:

        print()

        print(Fore.CYAN + "=" * 60)

        print(
            Fore.YELLOW
            + Style.BRIGHT
            + "📚 BOOKBUDDY LIBRARY MANAGEMENT SYSTEM".center(60)
        )

        print(Fore.CYAN + "=" * 60)

    @staticmethod
    def pause() -> None:

        input(
            Fore.GREEN
            + "\nPress ENTER to continue..."
        )

    @staticmethod
    def get_int(message: str) -> int:

        while True:

            try:

                return int(input(message))

            except ValueError:

                print(
                    Fore.RED
                    + "Please enter a valid integer."
                )

    @staticmethod
    def get_float(message: str) -> float:

        while True:

            try:

                return float(input(message))

            except ValueError:

                print(
                    Fore.RED
                    + "Please enter a valid number."
                )

    @staticmethod
    def success(message: str) -> None:

        print(
            Fore.GREEN
            + f"✔ {message}"
        )

    @staticmethod
    def error(message: str) -> None:

        print(
            Fore.RED
            + f"✖ {message}"
        )

    @staticmethod
    def info(message: str) -> None:

        print(
            Fore.CYAN
            + f"ℹ {message}"
        )

    # ==========================================
    # Menu
    # ==========================================

    def show_menu(self) -> None:

        self.title()

        print(Fore.GREEN + "1. Add Book")
        print("2. View Books")
        print("3. Add Reading Log")
        print("4. Reading Progress")
        print("5. Export Data")
        print("6. Import Data")
        print("7. Statistics")
        print(Fore.RED + "0. Exit")

        print()

            # ==========================================
    # Add Book
    # ==========================================

    def add_book(self) -> None:

        print()

        print("1. Physical Book")
        print("2. EBook")
        print("3. AudioBook")

        choice = input("\nChoose book type: ").strip()

        title = input("Title     : ").strip()
        author = input("Author    : ").strip()
        genre = input("Genre     : ").strip()
        pages = self.get_int("Pages     : ")

        if choice == "1":

            publisher = input("Publisher : ").strip()
            shelf = input("Shelf     : ").strip()

            book = PhysicalBook(
                title=title,
                author=author,
                genre=genre,
                pages=pages,
                publisher=publisher,
                shelf=shelf,
            )

        elif choice == "2":

            file_size = self.get_float("File Size (MB): ")
            file_format = input("Format         : ").strip()

            book = EBook(
                title=title,
                author=author,
                genre=genre,
                pages=pages,
                file_size=file_size,
                file_format=file_format,
            )

        elif choice == "3":

            duration = self.get_int("Duration (min): ")
            narrator = input("Narrator      : ").strip()
            audio_format = input("Audio Format  : ").strip()

            book = AudioBook(
                title=title,
                author=author,
                genre=genre,
                pages=pages,
                duration=duration,
                narrator=narrator,
                audio_format=audio_format,
            )

        else:

            self.error("Invalid book type.")

            return

        self.library.add_book(book)

        logger.info(f"Book added: {book.title}")

        self.success("Book added successfully.")

        self.pause()

    # ==========================================
    # View Books
    # ==========================================

    def view_books(self) -> None:

        books = self.library.list_books()

        print()

        if not books:

            self.info("Library is empty.")

            self.pause()

            return

        print("=" * 70)

        for index, book in enumerate(books, start=1):

            print(f"[{index}]")

            print(book)

            print("-" * 70)

        self.pause()

    # ==========================================
    # Reading Log
    # ==========================================

    def add_reading(self) -> None:

        print()

        title = input("Book title : ").strip()

        pages = self.get_int("Pages read : ")

        notes = input("Notes      : ").strip()

        self.tracker.log_reading(

            title=title,

            pages_read=pages,

            notes=notes,

        )

        logger.info(
            f"Reading log added for '{title}'"
        )

        self.success("Reading log saved.")

        self.pause()
    # ==========================================
    # Reading Progress
    # ==========================================

    def show_progress(self) -> None:

        print()

        self.progress.show_progress()

        self.pause()

    # ==========================================
    # Export Data
    # ==========================================

    def export_data(self) -> None:

        print()

        print("1. JSON")
        print("2. Pickle")

        choice = input("\nChoose format: ").strip()

        if choice == "1":
            fmt = "json"

        elif choice == "2":
            fmt = "pickle"

        else:

            self.error("Invalid format.")

            self.pause()

            return

        filename = input("Filename: ").strip()

        DataExporter.export(
            fmt,
            filename,
            self.library.list_books(),
        )

        logger.info(
            f"Export completed ({fmt}) -> {filename}"
        )

        self.success("Data exported successfully.")

        self.pause()

    # ==========================================
    # Import Data
    # ==========================================

    def import_data(self) -> None:

        print()

        print("1. JSON")
        print("2. Pickle")

        choice = input("\nChoose format: ").strip()

        if choice == "1":
            fmt = "json"

        elif choice == "2":
            fmt = "pickle"

        else:

            self.error("Invalid format.")

            self.pause()

            return

        filename = input("Filename: ").strip()

        books = DataExporter.import_data(
            fmt,
            filename,
        )

        self.library.clear()

        for book in books:

            self.library.add_book(book)

        logger.info(
            f"Import completed ({fmt}) <- {filename}"
        )

        self.success("Data imported successfully.")

        self.pause()

    # ==========================================
    # Statistics
    # ==========================================

    def statistics(self) -> None:

        stats = self.progress.statistics()

        print()

        print("=" * 45)

        print(
            Fore.CYAN
            + Style.BRIGHT
            + "LIBRARY STATISTICS"
        )

        print("=" * 45)

        print(
            f"Total Books       : {stats['total_books']}"
        )

        print(
            f"Completed Books   : {stats['completed_books']}"
        )

        print(
            f"In Progress       : {stats['in_progress']}"
        )

        print(
            f"Unread Books      : {stats['unread']}"
        )

        print(
            f"Total Pages       : {stats['total_pages']}"
        )

        print(
            f"Pages Read        : {stats['read_pages']}"
        )

        print(
            f"Overall Progress  : {stats['overall_progress']}%"
        )

        print(
            f"Average Progress  : {stats['average_progress']}%"
        )

        print("=" * 45)

        self.pause()
    # ==========================================
    # Main Loop
    # ==========================================

    def run(self) -> None:

        logger.info("Application started.")

        while self.running:

            try:

                self.show_menu()

                choice = input(
                    Fore.YELLOW + "Select option: "
                ).strip()

                actions = {

                    "1": self.add_book,

                    "2": self.view_books,

                    "3": self.add_reading,

                    "4": self.show_progress,

                    "5": self.export_data,

                    "6": self.import_data,

                    "7": self.statistics,

                    "0": self.exit_app,

                }

                action = actions.get(choice)

                if action is None:

                    self.error("Invalid option.")

                    self.pause()

                    continue

                action()

            except BookBuddyError as e:

                logger.error(str(e))

                self.error(str(e))

                self.pause()

            except KeyboardInterrupt:

                print()

                self.info("Interrupted by user.")

                self.exit_app()

            except Exception as e:

                logger.exception(e)

                self.error(f"Unexpected error: {e}")

                self.pause()

    # ==========================================
    # Exit
    # ==========================================

    def exit_app(self) -> None:

        logger.info("Application closed.")

        self.success("Thank you for using BookBuddy.")

        self.running = False


# ==========================================
# Program Entry Point
# ==========================================

def main():

    app = BookBuddyCLI()

    app.run()


if __name__ == "__main__":

    main()
        