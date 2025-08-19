from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from litestar import Litestar, Router
from litestar.response import Response
from litestar.static_files import StaticFilesConfig
from litestar.template import TemplateConfig
from litestar.contrib.jinja import JinjaTemplateEngine

from .api.views import health, index, messages_table
from .config.settings import Settings, get_settings
from .db.setup import init_db

logger = logging.getLogger(__name__)


def exception_handler(_: Any, exc: Exception) -> Response:
    """Handle unexpected exceptions."""

    logger.exception("Unhandled error", exc_info=exc)
    return Response("Internal Server Error", status_code=500)


def create_app(settings: Settings | None = None, *, create_tables: bool = False) -> Litestar:
    """Create and configure the Litestar application."""

    logging.basicConfig(level=logging.INFO)

    settings = settings or get_settings()
    init_db(settings, create_tables=create_tables)

    router = Router(path="", route_handlers=[index, messages_table, health])
    template_config = TemplateConfig(
        directory=Path(__file__).parent / "templates",
        engine=JinjaTemplateEngine,
    )
    static_config = [
        StaticFilesConfig(directories=[Path(__file__).parent / "static"], path="/static")
    ]

    return Litestar(
        route_handlers=[router],
        template_config=template_config,
        static_files_config=static_config,
        exception_handlers={Exception: exception_handler},
    )


try:  # pragma: no cover - handled during tests
    app = create_app()
except Exception as exc:  # pragma: no cover
    logger.warning("Failed to initialize application: %s", exc)
    # Fallback minimal application for import-time errors (e.g. missing configuration)
    app = Litestar([])
