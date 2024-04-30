import base64
import json
from typing import Any

from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response


def base64_filters(view_method):
    def decorator(self, *args, **kwargs):
        request = args[0]
        data: dict[str, Any] = request.GET.dict()
        base64_bytes: str = data.get("q", "")
        text: str = base64.b64decode(base64_bytes.encode("ISO-8859-1")).decode("ISO-8859-1")
        data: dict[str, Any] = dict(json.loads(text or '""'))
        request.data_base64 = data
        return view_method(self, *args, **kwargs)

    return decorator


def user_permission(permission: str, status: int = 403):
    def int_permission(func):
        def function(self, request, **kwargs):
            if permission == "superuser" and not request.user.is_superuser:
                return Response([_("You don't have access to the resource")], status=status)
            if not request.user.has_perm(permission):
                return Response([_("You don't have access to the resource")], status=status)
            return func(self, request, **kwargs)

        return function

    return int_permission

