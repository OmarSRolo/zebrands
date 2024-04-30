# -*- coding: utf-8 -*-
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission

from apps.products.dto.ProductsListDTO import ProductsDTO, ResponseProductsDTO, ResponseProductsListDTO
from apps.products.dto.swagger import ProductsFormDTO
from apps.products.services.ProductsService import ProductsService
from core.base.DTO import PaginateDTO, Pk, ResponseShortDTO
from core.misc.decorators import base64_filters, user_permission
from core.misc.utils import json_result, validate_image


class List(viewsets.ViewSet):
    parser_classes: list[type[MultiPartParser]] = [MultiPartParser]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes: list[type[BasePermission]] = [AllowAny, ]
        else:
            permission_classes: list[type[BasePermission]] = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @swagger_auto_schema(responses={"200": ResponseProductsDTO()})
    def retrieve(self, request, pk=None):
        repo: ProductsService = ProductsService().serializer(ProductsDTO, **{"request": request})
        query = repo.find_by(id=pk)
        return json_result(data=query, message="Producto obtenido")

    @swagger_auto_schema(request_body=Pk, responses={"200": ResponseShortDTO()})
    @user_permission("products.delete_products")
    def delete(self, request, pk=None):
        data: dict[str, Any] = request.data
        data['id'] = pk
        repo: ProductsService = ProductsService().serializer(ProductsDTO)
        info = repo.delete_by(id=pk)
        return json_result(data=info, message="Producto Eliminado")

    @swagger_auto_schema(query_serializer=PaginateDTO(), responses={"200": ResponseProductsListDTO()})
    @base64_filters
    def list(self, request, *args, **kwargs):
        data: dict[str, Any] = request.data_base64
        repo: ProductsService = ProductsService().serializer(ProductsDTO, **{"request": request})
        data["filters"] = data.get("filters", {})
        data["sort"] = data.get("sort", ["name"])
        soft: bool = data.get("filters", {}).pop("is_active", True)
        if soft:
            data["filters"].update({"category__is_active": soft})
        repo.find_all(**data, show_actives=soft)
        info = repo.paginate(limit=data.get("limit", 1000), offset=data.get("offset", 0))
        return json_result(message="Todos los productos", data={"results": info[0], "total": info[1]})

    @swagger_auto_schema(manual_parameters=ProductsFormDTO, responses={"200": ResponseProductsDTO()})
    @user_permission("products.change_products")
    def update(self, request, pk=None):
        validate_image(request.FILES.get("image", None))
        data: dict[str, Any] = request.data.dict()
        data['id'] = pk
        repo: ProductsService = ProductsService().serializer(ProductsDTO, **{"request": request})
        info = repo.update_by(**data, partial=True)
        return json_result(data=info, message="Producto editado")

    @swagger_auto_schema(manual_parameters=ProductsFormDTO, responses={"200": ResponseProductsDTO()})
    @user_permission("products.add_products")
    def insert(self, request):
        validate_image(request.FILES.get("image", None))
        data: dict[str, Any] = request.data.dict()
        repo: ProductsService = ProductsService().serializer(ProductsDTO, **{"request": request})
        info = repo.insert(**data)
        return json_result(data=info, message="Producto agregado")
