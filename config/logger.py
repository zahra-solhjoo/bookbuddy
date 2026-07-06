from __future__ import annotations

import logging
from pathlib import Path


# ----------------------------
# Log directory setup
# ----------------------------

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "bookbuddy.log"


# ----------------------------
# Logger factory
# ----------------------------

def get_logger(name: str = "BookBuddy") -> logging.Logger:

    logger = logging.getLogger(name)

    # prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# ----------------------------
# Global logger instance
# ----------------------------

logger = get_logger()