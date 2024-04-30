from abc import ABC, abstractmethod
from typing import Any


class Handler(ABC):

    def __init__(self, context: Any):
        self._context = context
        self._called: bool = False

    def is_called(self) -> bool:
        return self._called

    def non_attr_in_context_msg(self, var_names: [str]):
        return self._formatter_msg("The <{}> don't exits in to context !!!", var_names)

    def non_attr_in_params_msg(self, var_names: [str]):
        return self._formatter_msg("The <{}> don't exits in to params !!!", var_names)

    def _formatter_msg(self, text_msg, var_names: [str]):
        return str.format(text_msg, ", ".join(var_names))

    @abstractmethod
    def handle(self, params: dict):
        pass
