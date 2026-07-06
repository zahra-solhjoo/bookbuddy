class BookBuddyError(Exception):
    """
    Base exception for all custom errors in BookBuddy.
    """
    pass


class BookNotFoundError(BookBuddyError):
    """
    Raised when a book is not found in library.
    """
    pass


class DuplicateBookError(BookBuddyError):
    """
    Raised when trying to add a book that already exists.
    """
    pass


class InvalidLogError(BookBuddyError):
    """
    Raised when reading log data is invalid.
    """
    pass

class BookBuddyError(Exception):
    """Base exception for BookBuddy."""


class BookNotFoundError(BookBuddyError):
    """Raised when a book cannot be found."""
    pass


class DuplicateBookError(BookBuddyError):
    """Raised when a duplicate book is added."""
    pass


class InvalidBookError(BookBuddyError):
    """Raised when book data is invalid."""
    pass


class InvalidLogError(BookBuddyError):
    """Raised when reading log data is invalid."""
    pass


class ExportError(BookBuddyError):
    """Raised when exporting data fails."""
    pass


class ImportError(BookBuddyError):
    """Raised when importing data fails."""
    pass