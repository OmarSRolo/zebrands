from apps.categories.models import Categories
from core.base.BaseFactory import BaseFactory
import factory


class ProductsFactory(BaseFactory):
    sku: str = factory.Faker('uuid4')
    name: str = factory.Faker("pystr")
    brand: str = factory.Faker("pystr")
    description: str = factory.Faker('pystr')
    price: str = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    category: factory.Iterator = factory.Iterator(
        Categories.objects.filter(is_deleted=False, is_active=True).order_by("?"),
        getter=lambda c: c.pk)
