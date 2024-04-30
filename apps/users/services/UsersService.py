from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from apps.auth_system.models import Users
from apps.users.preconditions.users_preconditions import UsersPreconditions
from core.services.Service import Service


class UsersService(Service):
    """
    This class is a services that provides access to the users table in the database.
    """

    model: type[Users] = Users

    def save(self, **kwargs) -> Users:
        role_id: Group = kwargs.pop('role_id', None)
        if role_id:
            kwargs['role'] = role_id.name
        passw = kwargs.pop("password", False)
        if passw:
            kwargs["password"] = make_password(passw)
        user: Users = super(UsersService, self).save(**kwargs)
        user.groups.clear()
        user.groups.add(role_id)
        return user

    def update(self, model_object: Users, **kwargs) -> Users:
        role_id: Group = kwargs.pop('role_id', model_object.groups.first())
        kwargs['role'] = role_id.name
        passw = kwargs.pop("password", False)
        if passw:
            kwargs["password"] = make_password(passw)
        user: Users = super(UsersService, self).update(model_object, **kwargs)
        user.groups.clear()
        user.groups.add(role_id)
        return user

    def before_create(self, row):
        UsersPreconditions().users_preconditions(row)
        return row

    def before_update(self, instance, row):
        UsersPreconditions().users_preconditions(row)
        return row
