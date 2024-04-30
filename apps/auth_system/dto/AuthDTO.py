from rest_framework import serializers

from apps.auth_system.models import Users


class AuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
