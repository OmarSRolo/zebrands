from django.conf import settings
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.openapi import Swagger
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class V1APISchemeGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema: Swagger = super().get_schema(request, public)
        schema.base_path = '/api/v1/'
        return schema


schema_view_v1 = get_schema_view(
    openapi.Info(title="Zebrands API Protocol", default_version='v1', description="Zebrands API Protocol", ),
    public=True, permission_classes=[permissions.AllowAny, ], urlconf='project.urls.v1',
    url="https://organic-space-spork-w9x5wxvjq7439xj4-3031.app.github.dev/" if settings.ENVIRONMENT == 'DEV' else "http://localhost:8000",
    generator_class=V1APISchemeGenerator)
