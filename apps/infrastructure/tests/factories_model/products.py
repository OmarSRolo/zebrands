import factory

from apps.products.models import Products
from core.base.BaseFactory import BaseFactoryModel
from .categories import CategoriesFactoryModel


class ProductsFactoryModel(BaseFactoryModel):
    name: factory.Faker = factory.Faker("first_name")
    price: factory.Faker = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category: factory.Iterator = factory.SubFactory(CategoriesFactoryModel)

    class Meta:
        model: Products = Products
