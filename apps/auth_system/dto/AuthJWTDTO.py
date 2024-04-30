from django.utils.translation import gettext as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class LoginJWTResponseSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {"complete": True, "message": {"name": [_('Unable to log in with provided credentials.')]}}
    }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        token['id'] = user.id
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        group_name = []
        for group in self.user.groups.all():
            group_name.append(group.name)

        data['refresh'] = str(refresh)
        data['token'] = str(refresh.access_token)
        data["first_name"] = self.user.first_name
        data["last_name"] = self.user.last_name
        data["email"] = self.user.email
        data["user_id"] = self.user.pk
        data["role"] = self.user.role
        data["user"] = self.user
        data["phone"] = self.user.phone
        data["group_name"] = group_name
        data.pop("access")
        return data
