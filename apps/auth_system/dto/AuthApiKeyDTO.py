from rest_framework import serializers

from apps.auth_system.models import Users


class LoginApiKeyResponseSerializer(serializers.ModelSerializer):
    complete = serializers.BooleanField(default=True)
    token = serializers.CharField()
    user_id = serializers.CharField(source='pk')
    modules = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Users
        fields = (
            'complete', 'token', 'user_id', 'modules', 'phone', 'email', 'first_name', 'last_name', 'role')
