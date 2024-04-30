# -*- coding: utf-8 -*-
from typing import Any

from django.utils.translation import gettext as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission

from apps.categories.dto.CategoriesDTO import CategoriesDTO
from apps.categories.dto.swagger import ResponseCategoriesDTO, CategoriesFormDTO
from apps.categories.services.CategoriesInsertServices import CategoriesInsertService
from apps.categories.services.CategoriesServices import CategoriesService
from core.base.DTO import PaginateDTO, ResponseShortDTO
from core.misc.decorators import user_permission, base64_filters
from core.misc.utils import json_result, validate_image


class List(viewsets.ViewSet):
    parser_classes: list[type[MultiPartParser]] = [MultiPartParser, ]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == "retrieve":
            permission_classes: list[type[BasePermission]] = [AllowAny, ]
        else:
            permission_classes: list[type[BasePermission]] = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={"200": ResponseCategoriesDTO()})
    def retrieve(self, request, pk=None):
        repo: CategoriesService = CategoriesService().serializer(CategoriesDTO, **{"request": request})
        info = repo.find_by(id=pk)
        return json_result(data=info, message="Categoria Obtenida")

    @swagger_auto_schema(responses={"200": ResponseShortDTO()})
    @user_permission("categories.delete_categories")
    def delete(self, request, pk=None):
        repo: CategoriesService = CategoriesService()
        info = repo.delete_by(id=pk, soft=False)
        return json_result(data=info, message="Categoria Eliminada")

    @swagger_auto_schema(query_serializer=PaginateDTO(), responses={"200": CategoriesDTO(many=True)})
    @base64_filters
    def list(self, request):
        data: dict[str, Any] = request.data_base64
        repo: CategoriesService = CategoriesService().serializer(CategoriesDTO, **{"request": request})
        data["filters"] = data.get("filters", {})
        soft = data["filters"].pop("is_active", True)
        not_assigned = data["filters"].get("not_assigned", False)
        if not_assigned != "all":
            data["filters"]["not_assigned"] = not_assigned
        else:
            data["filters"].pop("not_assigned")
        repo.find_all(**data, show_actives=soft)
        info = repo.paginate(limit=data.get("limit", 100), offset=data.get("offset", 0))
        return json_result(message=_("All categories"), data={"results": info[0], "total": info[1]})

    @swagger_auto_schema(manual_parameters=CategoriesFormDTO, responses={"200": ResponseCategoriesDTO()})
    @user_permission("categories.add_categories")
    def insert(self, request):
        data = request.POST
        image = request.FILES.get("image", None)
        validate_image(image)
        info = {"image": image}
        repo: CategoriesInsertService = CategoriesInsertService().serializer(CategoriesDTO, **{"request": request})

        info.update({"name": data.get("name"), "is_active": True if data.get("is_active") == 'true' else False})

        result = repo.insert(**info)
        return json_result(data=result, message="Categoría agregada")

    @swagger_auto_schema(manual_parameters=CategoriesFormDTO, responses={"200": ResponseCategoriesDTO()})
    @user_permission("categories.change_categories")
    def update(self, request, pk=None):
        data: dict[str, Any] = request.data
        info: dict[str, Any] = {"image": None}

        info.update({"name": data["name"], "is_active": True if data.get("is_active") == 'true' else False, })
        info["id"] = pk
        repo: CategoriesInsertService = CategoriesInsertService().serializer(CategoriesDTO, **{"request": request})
        result = repo.update_by(**info, partial=True)
        return json_result(data=result, message="Categoria editada")
