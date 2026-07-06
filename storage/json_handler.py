from __future__ import annotations

import json
from pathlib import Path

from config.logger import logger
from models.book import Book
from models.book_factory import BookFactory
from utils.decorators import log_execution
from utils.retry import retry


class JSONHandler:

    @staticmethod
    @retry()
    @log_execution
    def save(
        filename: str,
        books: list[Book],
    ) -> None:

        path = Path(filename)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                [book.to_dict() for book in books],
                file,
                indent=4,
                ensure_ascii=False,
            )

        logger.info("Books exported to JSON.")

    @staticmethod
    @retry()
    @log_execution
    def load(
        filename: str,
    ) -> list[Book]:

        path = Path(filename)

        if not path.exists():
            return []

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        books = [
            BookFactory.create(item)
            for item in data
        ]

        logger.info("Books imported from JSON.")

        return books