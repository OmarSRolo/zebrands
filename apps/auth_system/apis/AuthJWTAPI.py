# -*- coding: utf-8 -*-
from typing import Any

from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.response import Response

from apps.auth_system.dto.AuthApiKeyDTO import LoginApiKeyResponseSerializer
from apps.auth_system.dto.AuthDTO import AuthTokenSerializer
from apps.auth_system.dto.swagger import LoginApiDTOSwagger, EmailDTOSwagger
from apps.auth_system.services.AuthJWTService import AuthJWTService
from core.base.DTO import ResponseShortDTO
from core.misc.utils import json_result


class AuthJWTAPI(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == 'get_permission':
            permission_classes: list[type[BasePermission]] = [IsAuthenticated]
        else:
            permission_classes: list[type[BasePermission]] = [AllowAny, ]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(request_body=AuthTokenSerializer, responses={"200": ResponseShortDTO()})
    def register(self, request, **kwargs):
        data: dict[str, Any] = request.data

        repo: AuthJWTService = AuthJWTService().serializer(AuthTokenSerializer)
        repo.register(**data)
        return json_result(data=True, message="Usuario Registrado")

    @swagger_auto_schema(request_body=LoginApiDTOSwagger, responses={"200": LoginApiKeyResponseSerializer()})
    def login(self, request, *args, **kwargs):
        repo: AuthJWTService = AuthJWTService()
        login = repo.login(request)
        return Response(login)

    @swagger_auto_schema(request_body=EmailDTOSwagger, responses={"200": ResponseShortDTO()})
    def check_user(self, request, *args, **kwargs):
        data: dict[str, Any] = request.data
        is_user_exist: bool = AuthJWTService().check_user(**data)
        if is_user_exist:
            return json_result(message="Email correcto", data="")
        return json_result(status=False, message="Email incorrecto, usuario no existe", data="")

    def get_permission(self, request, **kwargs):
        data: dict[str, Any] = request.data
        repo: AuthJWTService = AuthJWTService()
        data: dict[str, bool] = repo.get_permission_by_module(request.user, data.get("module", ""))
        return json_result(message="Permisos", data=data)

    @swagger_auto_schema(request_body=EmailDTOSwagger, responses={"200": ResponseShortDTO()})
    def reset_password(self, request, **kwargs):
        """ Genera una contraseña nueva

         Genera una contraseña nueva y la envía por email dado un email de un usuario.
        """
        data: dict[str, Any] = request.data
        data["from_email"] = settings.DEFAULT_FROM_EMAIL
        repo: AuthJWTService = AuthJWTService()
        repo.reset_password(data)
        return json_result(data="", message="Usuario obtenido")


@api_view(['GET'])
@permission_classes([])
@swagger_auto_schema(responses={"200": "True", "401": "False"})
def check(request):
    if not request.user.is_authenticated:
        return Response({"active": False}, status=401)
    response: Response = Response({"active": True}, status=200)
    return response
