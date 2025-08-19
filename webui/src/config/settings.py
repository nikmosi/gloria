from functools import lru_cache

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    """Database connection settings."""

    model_config = SettingsConfigDict(env_prefix="database_")

    dsn: str | None = None

    protocol: str = "postgres"
    user: str | None = None
    password: str | None = None
    host: str | None = None
    port: int | None = None
    database: str | None = None

    def make_dsn(self) -> str:
        """Return a DSN string for the configured database."""

        if self.dsn:
            return self.dsn

        return (
            f"{self.protocol}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(env_prefix="webui_", case_sensitive=False)

    database: Database = Database()


@lru_cache
def get_settings() -> "Settings":
    """Cached settings instance."""

    return Settings()
