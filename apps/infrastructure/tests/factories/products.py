from factory import Faker, django, SubFactory

from core.base.BaseFactory import BaseFactory
from .categories import CategoriesFactory


class ProductsFactory(BaseFactory):
    sku: str = Faker('uuid4')
    name: str = Faker("pystr")
    brand: str = Faker("pystr")
    description: str = Faker('pystr')
    price: str = Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category: SubFactory = SubFactory(CategoriesFactory)
