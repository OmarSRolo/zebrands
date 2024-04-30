from typing import Any

from core.base.workflows.handlers import Handler


class HandlerDefault(Handler):
    def __init__(self, context: Any):
        super().__init__(context)

    def handle(self, params: dict):
        self._called = True
