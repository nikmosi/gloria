import pytest
from pydantic import ValidationError
from pydantic_core import Url

from config.settings import Settings


def test_env_override(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("GLORIA_CLIENT_ID", "abc")
    monkeypatch.setenv("GLORIA_CLIENT_SECRET", "xyz")
    monkeypatch.setenv("GLORIA_PORT", "9999")
    monkeypatch.setenv("GLORIA_TARGET_CHANNELS", "foobar")
    monkeypatch.setenv(
        "GLORIA_DATABASE", "postgresql+asyncpg://test:test@localhost:5432/testdb"
    )
    monkeypatch.setenv("GLORIA_CALLBACK_URL", "http://example.com/callback")

    settings = Settings()

    assert settings.client_id == "abc"
    assert settings.client_secret == "xyz"
    assert settings.port == 9999
    assert settings.target_channels == "foobar"
    assert (
        settings.database.encoded_string()
        == "postgresql+asyncpg://test:test@localhost:5432/testdb"
    )
    assert settings.callback_url == Url("http://example.com/callback")


def test_invalid_database_url():
    with pytest.raises(ValidationError):
        Settings(database="not-a-valid-dsn")  # type: ignore


def test_invalid_callback_url():
    with pytest.raises(ValidationError):
        Settings(callback_url="not-a-url")  # type: ignore
