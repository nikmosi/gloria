from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from twitchAPI.type import AuthScope


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[".env.sample", ".env"], env_prefix="gloria_", case_sensitive=False
    )

    client_id: str = Field(default="...")
    client_secret: str = Field(default="...")
    target_channels: str = "jeensoff"
    user_scope: list[AuthScope] = [AuthScope.CHAT_READ]


settings = Settings()
