import logging

from loguru import logger

from config.settings import LogSettings
from infra.logging.logging import InterceptHandler, setup_logger


def test_setup_logger_default() -> None:
    settings = LogSettings(level="INFO")
    configured_logger = setup_logger(settings)
    assert configured_logger is not None
    assert logging.root.level == logging.INFO
    assert any(isinstance(h, InterceptHandler) for h in logging.root.handlers)


def test_setup_logger_json_mode() -> None:
    settings = LogSettings(level="DEBUG", json_format=True)
    configured_logger = setup_logger(settings)
    assert configured_logger is not None
    assert logging.root.level == logging.DEBUG


def test_intercept_handler_routes_to_loguru() -> None:
    setup_logger(LogSettings(level="INFO"))
    std_logger = logging.getLogger("test_intercept_logger")
    # Should execute without error
    std_logger.info("Test intercepted log message")
    logger.info("Test direct loguru message")
