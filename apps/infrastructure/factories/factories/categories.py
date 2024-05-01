import factory

from core.base.BaseFactory import BaseFactory


class CategoriesFactory(BaseFactory):
    name: factory.Faker = factory.Faker('pystr')
