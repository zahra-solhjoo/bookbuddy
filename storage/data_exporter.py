from __future__ import annotations

from models.book import Book

from storage.json_handler import JSONHandler
from storage.pickle_handler import PickleHandler


class DataExporter:
    """
    Handles importing and exporting books
    using different storage formats.
    """

    _handlers = {
        "json": JSONHandler,
        "pickle": PickleHandler,
    }

    @classmethod
    def export(
        cls,
        fmt: str,
        filename: str,
        books: list[Book],
    ) -> None:

        fmt = fmt.lower()

        handler = cls._handlers.get(fmt)

        if handler is None:
            raise ValueError(
                f"Unsupported export format: {fmt}"
            )

        handler.save(filename, books)

    @classmethod
    def import_data(
        cls,
        fmt: str,
        filename: str,
    ) -> list[Book]:

        fmt = fmt.lower()

        handler = cls._handlers.get(fmt)

        if handler is None:
            raise ValueError(
                f"Unsupported import format: {fmt}"
            )

        return handler.load(filename)

    @classmethod
    def supported_formats(cls) -> list[str]:
        """
        Returns supported file formats.
        """

        return list(cls._handlers.keys())