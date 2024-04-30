from abc import ABC
from typing import Any

from core.base.workflows.handlers.handler import Handler


def move_to_next_handler(function):
    def wrapper(self, params: dict):
        function(self, params)
        self._called = True
        self.next_handler.handle(params)

    return wrapper


class HandlerAddon(Handler, ABC):
    def __init__(self, context: Any, next_handler: Handler):
        super().__init__(context)
        self.next_handler: Handler = next_handler
