from typing import Any

from .handler import Handler
from .handler_default import HandlerDefault


class HandlersContext[T]:
    def __init__(self):
        self._head: Handler = HandlerDefault(self)
        self._handler: Handler = self._head
        self._attrs: dict = {}

    def is_finish(self) -> bool:
        return self._head.is_called()

    def has_attr(self, key: str) -> bool:
        return key in self._attrs

    def get_attr(self, key: str) -> Any | None:
        return self._attrs[key] if key in self._attrs else None

    def set_attr(self, key: str, value: Any):
        self._attrs[key] = value

    def get_attr_name_list(self) -> [str]:
        return list(self._attrs.keys())

    def set_attrs(self, attrs: dict[str, Any]):
        self._attrs |= attrs

    def push_handler(self, type_var: type(T)):
        self._handler = type_var(self, self._handler)

    def handle(self, params: dict):
        self._handler.handle(params)
