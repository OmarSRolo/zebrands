from rest_framework import serializers


class LoginApiDTOSwagger(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class EmailDTOSwagger(serializers.Serializer):
    email = serializers.EmailField()
