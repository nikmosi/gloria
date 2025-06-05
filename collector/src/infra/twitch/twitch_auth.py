from typing import cast

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse, RedirectResponse
from loguru import logger
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.twitch import Twitch
from twitchAPI.type import TwitchAPIException
from uvicorn import Config, Server

from config import Settings


async def authenticate(settings: Settings) -> Twitch:
    logger.debug("authenticate starting")
    twitch = await Twitch(app_id=settings.client_id, app_secret=settings.client_secret)
    auth = UserAuthenticator(
        twitch, scopes=settings.user_scope, url=settings.callback_url
    )

    app = FastAPI()
    server_ref = {}

    logger.debug("init")

    @app.get("/login")
    async def login():
        return RedirectResponse(auth.return_auth_url())

    @app.get("/login/confirm")
    async def login_confirm(request: Request):
        state = request.query_params.get("state")
        if state != auth.state:
            return PlainTextResponse("Bad state", status_code=401)
        code = request.query_params.get("code")
        if code is None:
            return PlainTextResponse("Missing code", status_code=400)
        try:
            token, refresh = cast(
                tuple[str, str], await auth.authenticate(user_token=code)
            )
            await twitch.set_user_authentication(token, settings.user_scope, refresh)
        except TwitchAPIException:
            return PlainTextResponse("Auth failed", status_code=400)

        # Завершаем сервер
        server_ref["server"].should_exit = True
        return PlainTextResponse("Auth complete. You can close this tab.")

    config = Config(app=app, host="0.0.0.0", port=settings.port, log_level="info")
    server = Server(config)
    server_ref["server"] = server

    logger.info(f"Open http://localhost:{settings.port}/login in your browser")

    await server.serve()
    logger.info("authenticate [bold green]complete[/]")
    return twitch
