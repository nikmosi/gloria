from infra.twitch.exceptions.base import BaseTwitchError


class StateError(BaseTwitchError):
    pass


class CodeError(BaseTwitchError):
    pass
