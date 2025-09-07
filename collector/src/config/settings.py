from pathlib import Path

from pydantic import BaseModel, Field, PostgresDsn
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict
from twitchAPI.type import AuthScope


class LogSettings(BaseModel):
    level: str = "DEBUG"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.sample", ".env"],
        env_prefix="gloria_",
        case_sensitive=False,
        env_nested_delimiter="_",
    )

    client_id: str = Field(default="...")
    client_secret: str = Field(default="...")
    target_channels: str = "jeensoff"
    user_scope: list[AuthScope] = [AuthScope.CHAT_READ]

    filtered_name: list[str] = ["gloria_bot", "nikmosi"]

    callback_url: Url = Url("http://localhost/login/confirm")
    port: int = 8000

    database: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://user:123@postgres:5432/collector"
    )

    storage_path: Path = Path("./var/collector/token.json")

    log: LogSettings = Field(default_factory=LogSettings)
