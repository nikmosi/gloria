from typing import Annotated

from litestar import Controller, MediaType, get, status_codes
from litestar.params import Parameter
from litestar.response import Redirect, Response
from loguru import logger
from twitchAPI.type import TwitchAPIException

from infra.twitch.exceptions import CodeError, StateError
from infra.twitch.services import AuthService


class AuthController(Controller):
    @get("/login")
    async def login(self, auth_service: AuthService) -> Redirect:
        logger.debug("generating auth link")
        return Redirect(auth_service.get_link())

    @get("/login/confirm", media_type=MediaType.TEXT)
    async def login_confirm(
        self,
        code: str,
        state_: Annotated[str, Parameter(query="state")],
        auth_service: AuthService,
    ) -> Response[str]:
        logger.debug("compliting auth")
        try:
            await auth_service.verify(code, state_)
        except TwitchAPIException:
            return Response(
                "Auth failed", status_code=status_codes.HTTP_400_BAD_REQUEST
            )
        except StateError:
            return Response("Bad state", status_code=status_codes.HTTP_401_UNAUTHORIZED)
        except CodeError:
            return Response(
                "Missing code", status_code=status_codes.HTTP_400_BAD_REQUEST
            )
        auth_service.complete()
        logger.info("complete auth")
        return Response(
            "Auth complete. You can close this tab.",
        )
