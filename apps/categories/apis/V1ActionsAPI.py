import json
from typing import Any

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.categories.dto.CategoriesDTO import CategoriesDTO
from apps.categories.services.CategoriesServices import CategoriesService
from core.base.DTO import ResponseShortDTO, pk__in, Pk
from core.misc.decorators import user_permission
from core.misc.utils import json_result


class V1ActionsAPI(viewsets.ViewSet):
    @swagger_auto_schema(request_body=pk__in, responses={"200": ResponseShortDTO()})
    @user_permission("categories.delete_categories")
    def delete_all(self, request):
        data = json.loads(request.body)
        repo: CategoriesService = CategoriesService().serializer(CategoriesDTO)
        info = repo.delete_all(**data, soft=False)
        return json_result(data=info, message="Categorías Eliminadas")

    @swagger_auto_schema(request_body=Pk, responses={"200": ResponseShortDTO()})
    @user_permission("categories.delete_categories")
    def restore(self, request):
        data: dict[str, Any] = request.data
        repo: CategoriesService = CategoriesService().serializer(CategoriesDTO)
        info = repo.restore_by(**data)
        return json_result(data=info, message="Categoría Restaurada")

    @swagger_auto_schema(request_body=pk__in, responses={"200": ResponseShortDTO()})
    @user_permission("categories.delete_categories")
    def restore_all(self, request):
        data: dict[str, Any] = request.data
        repo: CategoriesService = CategoriesService().serializer(CategoriesDTO)
        info = repo.restore_all(**data)
        return json_result(data=info, message="Categorías Restauradas")
