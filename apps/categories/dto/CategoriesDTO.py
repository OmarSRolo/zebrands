# -*- coding: utf-8 -*-
from apps.categories.models import Categories
from rest_framework import serializers


class CategoriesDTO(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=True, allow_empty_file=True, required=False)

    class Meta:
        model = Categories
        exclude = ('deleted_at', "is_deleted")
