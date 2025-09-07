from __future__ import annotations

import shutil

import loguru
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler

from config.settings import LogSettings


def setup_logger(settings: LogSettings) -> loguru.Logger:
    terminal_width = shutil.get_terminal_size((220, 20)).columns
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(
                    console=Console(force_terminal=True, width=terminal_width),
                    markup=True,
                    rich_tracebacks=True,
                    omit_repeated_times=False,
                ),
                "format": "{message}",
                "level": settings.level,
            }
        ]
    )

    return logger
