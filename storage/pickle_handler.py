from __future__ import annotations

import pickle
from pathlib import Path

from models.book import Book
from config.logger import logger
from utils.decorators import log_execution
from utils.retry import retry


class PickleHandler:

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

        with path.open("wb") as file:

            pickle.dump(
                books,
                file,
                protocol=pickle.HIGHEST_PROTOCOL,
            )

        logger.info("Books exported to Pickle.")

    @staticmethod
    @retry()
    @log_execution
    def load(
        filename: str,
    ) -> list[Book]:

        path = Path(filename)

        if not path.exists():
            return []

        with path.open("rb") as file:

            books = pickle.load(file)

        logger.info("Books imported from Pickle.")

        return books