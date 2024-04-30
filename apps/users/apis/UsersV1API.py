from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.users.dto.UsersDTO import ReadUsersDTO, UsersDTO, ResponseUsersDTO, ResponseUsersListDTO
from apps.users.services.UsersService import UsersService
from core.base.DTO import ResponseShortDTO, PaginateDTO, pk__in, Pk
from core.misc.decorators import base64_filters, user_permission
from core.misc.utils import json_result


class List(viewsets.ViewSet):
    @swagger_auto_schema(responses={"200": ResponseUsersDTO()})
    @user_permission("auth_system.view_users")
    def retrieve(self, request, pk=None, **kwargs):
        repo: UsersService = UsersService().serializer(ReadUsersDTO)
        query = repo.find_by(id=pk)
        return json_result(data=query, message="Usuario obtenido")

    @swagger_auto_schema(responses={"200": ResponseShortDTO()})
    @user_permission("auth_system.delete_users")
    def delete(self, request, pk=None, **kwargs):
        data: dict[str, Any] = request.data
        data['id'] = pk
        repo: UsersService = UsersService().serializer(UsersDTO)
        repo.delete_by(**data, soft=False)
        return json_result(data=True, message="Usuario Eliminado")

    @swagger_auto_schema(query_serializer=PaginateDTO(), responses={"200": ResponseUsersListDTO()})
    @user_permission("auth_system.view_users")
    @base64_filters
    def list(self, request, **kwargs):
        repo: UsersService = UsersService().serializer(ReadUsersDTO)
        data: dict[str, Any] = request.data_base64
        data["filters"]["is_staff"] = False
        repo.find_all(**data)
        info = repo.paginate(limit=data.get("limit", 1000), offset=data.get("offset", 0))
        return json_result(message="Todos los Usuarios", data={"results": info[0], "total": info[1]})

    @swagger_auto_schema(request_body=UsersDTO, responses={"200": ResponseUsersDTO()})
    @user_permission("auth_system.add_users")
    def insert(self, request, **kwargs):
        data: dict[str, Any] = request.data
        repo: UsersService = UsersService().serializer(UsersDTO)
        info = repo.insert(**data, return_object=True)
        result = repo.serializer(ReadUsersDTO).get_data(info)
        return json_result(data=result, message="Usuario agregado")

    @swagger_auto_schema(request_body=UsersDTO, responses={"200": ResponseUsersDTO()})
    @user_permission("auth_system.change_users")
    def update(self, request, pk=None, **kwargs):
        data: dict[str, Any] = request.data
        data['id'] = pk
        repo: UsersService = UsersService().serializer(UsersDTO)
        info = repo.update_by(**data, partial=True, return_object=True)
        result = repo.serializer(ReadUsersDTO).get_data(info)
        return json_result(data=result, message="Usuario editado")

    @swagger_auto_schema(request_body=pk__in, responses={"200": ResponseShortDTO()})
    @user_permission("auth_system.delete_users")
    def delete_all(self, request, **kwargs):
        data: dict[str, Any] = request.data
        repo: UsersService = UsersService().serializer(UsersDTO)
        repo.delete_all(**data, soft=False)
        return json_result(data=True, message="Usuarios Eliminados")

    @swagger_auto_schema(request_body=Pk, responses={"200": ResponseShortDTO()})
    @user_permission("auth_system.delete_users")
    def restore(self, request, **kwargs):
        data: dict[str, Any] = request.data
        repo: UsersService = UsersService().serializer(UsersDTO)
        info = repo.restore_by(**data)
        return json_result(data=info, message="Usuario Restaurado")

    @swagger_auto_schema(request_body=pk__in, responses={"200": ResponseShortDTO()})
    @user_permission("auth_system.delete_users")
    def restore_all(self, request, **kwargs):
        data: dict[str, Any] = request.data
        repo: UsersService = UsersService().serializer(UsersDTO)
        info = repo.restore_all(**data)
        return json_result(data=info, message="Usuarios Restaurados")
