from __future__ import annotations

import inspect
import logging
import shutil
import sys
from typing import Any, cast

import loguru
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

from config.settings import LogSettings


class InterceptHandler(logging.Handler):
    """Intercept standard logging messages and route them to loguru."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level: str | int = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame = inspect.currentframe()
        depth = 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logger(settings: LogSettings) -> loguru.Logger:
    terminal_width = shutil.get_terminal_size((220, 20)).columns

    if settings.json_format:
        handlers: list[dict[str, Any]] = [
            {
                "sink": sys.stdout,
                "serialize": True,
                "level": settings.level,
            }
        ]
    else:
        handlers = [
            {
                "sink": RichHandler(
                    console=Console(force_terminal=True, width=terminal_width),
                    markup=False,
                    rich_tracebacks=True,
                    omit_repeated_times=False,
                ),
                "format": "{message}",
                "level": settings.level,
            }
        ]

    logger.configure(handlers=cast(Any, handlers))

    # Intercept standard library logging
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(settings.level)

    # Ensure third-party loggers route through InterceptHandler
    # without duplicate propagation
    for logger_name in ("uvicorn", "uvicorn.access", "twitchAPI", "sqlalchemy.engine"):
        std_log = logging.getLogger(logger_name)
        std_log.handlers = [InterceptHandler()]
        std_log.propagate = False

    return logger
