import uuid

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.serializers import Serializer

from apps.auth_system.dto.AuthJWTDTO import LoginJWTResponseSerializer
from apps.auth_system.models import Users
from core.misc.Enums import LIST_INTERNALS_MODULES
from core.services.EmailService import BasicEmail
from core.services.Service import Service
from cronjobs.tasks import send_email


class AuthJWTService(Service):
    model = type[Users]

    def get_permissions_from_user(self, user: Users):
        permissions = user.get_all_permissions()
        list_modules: list[str] = []
        for modules in permissions:
            if modules.__contains__(".view"):
                mod = modules.split(".")[0]
                if mod not in LIST_INTERNALS_MODULES:
                    list_modules.append(mod)
        return list(set(list_modules))

    def register(self, **kwargs):
        data: Serializer = self._serializer(data=kwargs)
        if data.is_valid():
            try:
                p: Group = Group.objects.get(name="Clients")
                data_saved = Users.objects.create_user(**kwargs)
                data_saved.groups.add(p)
                data_saved.role = p.name
                data_saved.save()
                return kwargs
            except Group.DoesNotExist:
                raise serializers.ValidationError(
                    {"complete": True, "message": {"name": [_("The group Clients does not exist")]}})
        else:
            raise serializers.ValidationError(data.errors, code='authorization')

    def get_permission_by_module(self, user: Users, module_sent: str) -> dict[str, bool]:
        permissions = user.get_all_permissions()
        data: dict[str, bool] = {}
        for perm in permissions:
            module, permission = perm.split('.')
            if module == module_sent:
                module_ = permission.split("_")[0]
                data[module_] = True
        return data

    def reset_password(self, data):
        from_email = data.pop('from_email')
        user = self.find_by(**data, return_object=True)
        if not user:
            raise serializers.ValidationError({"info": _("User not found")})
        new_password: str = str(uuid.uuid4()).split("-")[0]
        user.password = make_password(new_password)
        user.save()
        context: dict[str, str] = {"image": '', 'password': new_password}
        email: BasicEmail = BasicEmail(subject='Zebrands: Nueva contraseña solicitada', from_email=from_email,
                                       to_email=[data['email']], template='email.txt', context=context, message="")
        send_email.delay(email.as_dict())

    def check_user(self, **kwargs):
        return Users.objects.filter(email=kwargs["email"], is_active=True, is_deleted=False).exists()

    def login(self, request):
        serializer: LoginJWTResponseSerializer = LoginJWTResponseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.pop("user")
        list_of_permissions = self.get_permissions_from_user(user)
        serializer.validated_data['modules'] = list_of_permissions
        serializer.validated_data["complete"] = True
        return serializer.validated_data
