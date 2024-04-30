import factory

from core.base.BaseFactory import BaseFactory


class UsersFactory(BaseFactory):
    first_name: factory.Faker = factory.Faker('first_name')
    last_name: factory.Faker = factory.Faker('first_name')
    email: factory.Faker = factory.Faker('email')
