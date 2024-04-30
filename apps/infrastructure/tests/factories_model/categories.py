import factory

from core.base.BaseFactory import BaseFactoryModel
from apps.categories.models import Categories


class CategoriesFactoryModel(BaseFactoryModel):
    class Meta:
        model: type[Categories] = Categories

    name: factory.Faker = factory.Faker('pystr')
    image: factory.django.ImageField = factory.django.ImageField(color='blue')
