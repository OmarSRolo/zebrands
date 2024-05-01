import factory

from core.base.BaseFactory import BaseFactoryModel
from apps.auth_system.models import Users


class UsersFactoryModel(BaseFactoryModel):
    class Meta:
        model: type[Users] = Users

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('first_name')
    email = factory.Faker('email')
