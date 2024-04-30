from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.base.DTO import ResponseDTO
from apps.auth_system.models import Users


class ReadUsersDTO(serializers.ModelSerializer):
    role_id = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model: type[Users] = Users
        fields: list[str] = [
            'username', 'first_name', 'last_name', 'email', 'id', 'address', 'role_id', 'role', 'phone', 'is_active', ]

    def get_role_id(self, obj):
        superuser = obj.is_superuser
        if superuser:
            return 0
        group = obj.groups.all().first().pk
        return group

    def get_role(self, obj):
        superuser = obj.is_superuser
        if superuser:
            return 0
        group = obj.groups.all().first().name
        return group


class UsersDTO(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)
    email = serializers.EmailField(required=False,
                                   validators=[
                                       UniqueValidator(queryset=Users.objects.filter(is_deleted=False, is_active=True),
                                                       message=[_("This is already exists a user with that email")])])
    password = serializers.CharField(required=False)

    class Meta:
        model: type[Users] = Users
        fields: list[str] = [
            'username', 'first_name', 'last_name', 'email', 'id', 'address', 'role_id', 'role', 'phone', 'is_active',
            'password']


class ResponseUsersDTO(ResponseDTO):
    data = ReadUsersDTO()


class ResultsPaginateUsersDTO(serializers.Serializer):
    results = ReadUsersDTO(many=True)
    total = serializers.IntegerField()


class ResponseUsersListDTO(ResponseDTO):
    data = ResultsPaginateUsersDTO()
