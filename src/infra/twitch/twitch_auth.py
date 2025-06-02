from typing import cast

from loguru import logger
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch

from config import Settings


async def authenticate(settings: Settings) -> Twitch:
    logger.debug("Authenticate start")
    twitch = await Twitch(app_id=settings.client_id, app_secret=settings.client_secret)
    auth = UserAuthenticator(twitch, settings.user_scope)
    token, refresh_token = cast(tuple[str, str], await auth.authenticate())

    await twitch.set_user_authentication(token, settings.user_scope, refresh_token)
    logger.info("Authenticate is complete")

    return twitch
