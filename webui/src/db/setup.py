from __future__ import annotations

from urllib.parse import urlparse

from . import db
from ..config.settings import Settings


def init_db(settings: Settings, *, create_tables: bool = False) -> None:
    """Bind database using settings and generate mappings."""

    dsn = settings.database.make_dsn()
    parsed = urlparse(dsn)
    provider = parsed.scheme

    if provider in ("postgresql", "postgres"):
        provider = "postgres"
        db.bind(
            provider=provider,
            user=parsed.username,
            password=parsed.password,
            host=parsed.hostname,
            port=parsed.port,
            database=parsed.path.lstrip("/"),
        )
    elif provider == "sqlite":
        filename = parsed.path or ":memory:"
        db.bind(provider="sqlite", filename=filename, create_db=create_tables)
    else:
        raise ValueError(f"Unsupported database provider: {provider}")

    db.generate_mapping(create_tables=create_tables)
