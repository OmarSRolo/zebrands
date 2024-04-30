# -*- coding: utf-8 -*-
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.products.dto.ProductsListDTO import ProductsDTO
from core.base.DTO import ResponseShortDTO, pk__in
from core.misc.decorators import user_permission
from core.misc.utils import json_result
from apps.products.services.ProductsService import ProductsService


class V1ActionsAPI(viewsets.ViewSet):

    @swagger_auto_schema(request_body=pk__in, responses={"200": ResponseShortDTO()})
    @user_permission("products.delete_products")
    def delete_all(self, request):
        data: dict[str, Any] = request.data
        repo: ProductsService = ProductsService().serializer(ProductsDTO)
        info = repo.delete_all(**data)
        return json_result(data=info, message="Productos Eliminados")
