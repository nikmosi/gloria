from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    model_config = SettingsConfigDict(env_prefix="database_")

    dsn: str | None

    protocol: str = "postgresql+asyncpg"
    user: str
    password: str
    host: str
    port: str
    database: str

    def make_dsn(self):
        if self.dsn:
            return self.dsn

        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="webui_", case_sensitive=False)
    database: Database
