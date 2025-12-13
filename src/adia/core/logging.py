import logging
import sys

from adia.core.config import get_settings


def setup_logging() -> None:
    settings = get_settings()

    level = settings.LOG_LEVEL.upper()

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
