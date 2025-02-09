from typing import Iterable
from litestar.handlers import BaseRouteHandler


class Endpoint:
    _handlers: Iterable[BaseRouteHandler]

    def __init__(self, hanlders: Iterable[BaseRouteHandler]):
        self._handlers = hanlders

    def __iter__(self):
        return iter(self._handlers)
