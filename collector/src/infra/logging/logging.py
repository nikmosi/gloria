import shutil

from loguru import logger
from rich.console import Console
from rich.logging import RichHandler


def setup_logger() -> None:
    terminal_width = shutil.get_terminal_size((220, 20)).columns
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(
                    console=Console(force_terminal=True, width=terminal_width),
                    markup=True,
                    rich_tracebacks=True,
                ),
                "format": "{message}",
            }
        ]
    )
