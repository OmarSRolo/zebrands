from rest_framework import serializers

from apps.products.models import Products
from core.base.DTO import ResponseDTO


class ProductsDTO(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, allow_empty_file=True, required=False)
    category_name = serializers.CharField(source='category.name', required=False)

    class Meta:
        model: type[Products] = Products
        exclude: list[str] = ['deleted_at', "is_deleted", "created_at", "updated_at"]


class ResponseProductsDTO(ResponseDTO):
    data = ProductsDTO()


class PProductsDTO(serializers.Serializer):
    results = ProductsDTO()
    total = serializers.IntegerField()


class ResponseProductsListDTO(ResponseDTO):
    data = PProductsDTO()
