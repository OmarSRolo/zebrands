from rest_framework import serializers


class PaginateDTO(serializers.Serializer):
    q = serializers.CharField(required=False)

    class Meta:
        swagger_schema_fields: dict[str, str] = {
            'title': 'Paginator',
            'description': 'Pagina y filtra los modelos',
        }


class Pk(serializers.Serializer):
    id = serializers.IntegerField()


class pk__in(serializers.Serializer):
    id = serializers.ListField(child=serializers.IntegerField())


class ResponseDTO(serializers.Serializer):
    complete = serializers.BooleanField()
    message = serializers.CharField(max_length=250)


class ResponseShortDTO(ResponseDTO):
    data = serializers.BooleanField()
