from drf_yasg import openapi

ProductsFormDTO = [
    openapi.Parameter("image", in_=openapi.IN_FORM, description="Foto", type=openapi.TYPE_FILE),
    openapi.Parameter("name", in_=openapi.IN_FORM, description="Nombre", type=openapi.TYPE_STRING),
    openapi.Parameter("category", in_=openapi.IN_FORM, description="Categoria", type=openapi.TYPE_INTEGER),
    openapi.Parameter("description", in_=openapi.IN_FORM, description="Descripcion", type=openapi.TYPE_STRING),
]
