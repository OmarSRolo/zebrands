from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.auth_system.models import Users


class UsersPreconditions:

    def users_preconditions(self, row):
        if 'email' in row:
            email: str = row["email"]

            queryset: QuerySet[Users] = Users.objects.filter(is_active=True, is_deleted=False, email=email)

            if 'id' in row:
                queryset: QuerySet[Users] = queryset.exclude(pk=row['id'])

            if queryset:
                raise serializers.ValidationError(
                    {"complete": True, "message": {"email": [_("There is already a user with this email")]}})
