from rest_framework import serializers
from drf_yasg import openapi

from core.base.DTO import ResponseDTO
from apps.categories.dto.CategoriesDTO import CategoriesDTO


class ResponseCategoriesDTO(ResponseDTO):
    data = CategoriesDTO()


class ResultsPaginateCategoriesDTO(serializers.Serializer):
    results = CategoriesDTO(many=True)
    total = serializers.IntegerField()


class ResponseCategoriesListDTO(ResponseDTO):
    data = ResultsPaginateCategoriesDTO()


CategoriesFormDTO = [
    openapi.Parameter("image", in_=openapi.IN_FORM, description="Foto", type=openapi.TYPE_FILE),
    openapi.Parameter("name", in_=openapi.IN_FORM, description="Nombre", type=openapi.TYPE_STRING),
]
