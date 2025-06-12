from litestar import Litestar
from litestar.di import Provide
from loguru import logger
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from uvicorn import Config, Server

from config import Settings
from infra.utils.dependencies import WrapVar

from .controllers import AuthController
from .services import AuthService


async def authenticate(settings: Settings) -> Twitch:
    logger.debug("authenticate starting")
    twitch: Twitch = await Twitch(
        app_id=settings.client_id, app_secret=settings.client_secret
    )
    auth = UserAuthenticator(
        twitch, scopes=settings.user_scope, url=settings.callback_url.unicode_string()
    )

    auth_service = AuthService(settings.user_scope, auth, twitch)
    app = Litestar(
        dependencies={"auth_service": Provide(WrapVar(auth_service))},
        route_handlers=[AuthController],
    )

    config = Config(app=app, host="0.0.0.0", port=settings.port, log_level="info")
    server = Server(config)

    auth_service.subscribe_on_complete(lambda: setattr(server, "should_exit", True))

    logger.info("run uvicorn")
    await server.serve()

    logger.info("authenticate [bold green]complete[/]")
    return twitch
