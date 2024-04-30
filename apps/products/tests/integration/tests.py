from decimal import Decimal

from django.db.models import QuerySet
from parameterized import parameterized

from apps.infrastructure.tests.factories import ProductsFactory
from apps.infrastructure.tests.factories_model.categories import CategoriesFactoryModel
from apps.products.dto.ProductsListDTO import ProductsDTO
from apps.products.models import Products
from apps.products.services.ProductsService import ProductsService
from core.tests.IntegrationTest import IntegrationTest


class ProductsTest(IntegrationTest):
    fixtures = ['test/users.json', 'products_categories.json', 'products_products.json']

    def setUp(self):
        super(ProductsTest, self).setUp()
        # Creo 5 categorias nuevas en BD
        self.categories = CategoriesFactoryModel.create_batch(5)
        self.service = ProductsService()
        self.serializer = ProductsDTO

    @parameterized.expand([
        ("tomate", "2.50", "description"),
        ("mayonesa", "3.90", "description_1"),
    ])
    def test_create(self, name: str, prod_price: Decimal,
                    prod_description: str):
        repo = self.service.serializer(self.serializer)
        # Obtengo al azar una de ella
        product_dict = ProductsFactory.create(price=prod_price, description=prod_description, qty=0, name=name)
        product_dict['category'] = self.categories[0].pk
        product_saved: Products = repo.insert(**product_dict, return_object=True)
        self.assertEqual(product_saved.price, Decimal(prod_price).quantize(Decimal('.01')))
        self.assertEqual(product_saved.name, name)
        self.assertEqual(product_saved.description, prod_description)
        self.assertEqual(product_saved.category_id, product_dict['category'])

    def test_get(self):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        products = Products.objects.last()
        res = repo.find_by(id=products.pk, return_object=True)
        self.assertEqual(res.id, products.pk)
        self.assertEqual(res.name, products.name)

    @parameterized.expand([
        ({"filters": {}, "limit": 1, "offset": 0, "order": "asc", "sort": ["pk"]}, False,),
        ({"filters": {}, "limit": 2, "offset": 0, "order": "desc", "sort": ["pk"]}, True,)
    ])
    def test_list(self, data, show_actives_values: bool):
        if show_actives_values:
            total = Products.objects.filter(is_active=True, is_deleted=False).count()
        else:
            total = Products.objects.filter(is_deleted=False).count()

        repo = self.service.serializer(self.serializer, **{"request": self.request})
        repo.find_all(**data, show_actives=show_actives_values)
        info = repo.paginate(limit=data["limit"], offset=data["offset"])
        self.assertEqual(total, info[1])
        self.assertEqual(len(info[0]), data["limit"])

    @parameterized.expand([
        ("tomates",),
        ("papas",)
    ])
    def test_update(self, prod_name: str):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        products = Products.objects.filter(is_active=True, is_deleted=False).last()
        product_dict = ProductsFactory.create(name=prod_name)
        product_dict['id'] = products.pk
        product_dict['category'] = self.categories[0].pk
        repo.update_by(**product_dict)
        products.refresh_from_db()
        self.assertEqual(products.name, prod_name)

    def test_delete(self):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        products = Products.objects.last()
        repo.delete_by(**{"id": products.pk})
        products = Products.objects.last()
        self.assertEqual(products.is_active, False)

    def test_delete_all(self):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        ids: list[int] = [x.id for x in Products.objects.all()]
        repo.delete_all(**{"id__in": ids})
        all_products: QuerySet[Products] = Products.objects.all()
        f: bool = True
        for tab in all_products:
            if tab.is_active:
                f: bool = False
        self.assertEqual(f, True)

    def test_restore(self):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        products = Products.objects.filter(is_active=False).first()
        products.is_active = False
        products.save()
        repo.restore_by(**{"id": products.pk})
        products.refresh_from_db()
        self.assertEqual(products.is_active, True)

    def test_restore_all(self):
        repo = self.service.serializer(self.serializer, **{"request": self.request})
        ids: list[int] = [x.id for x in Products.objects.filter(is_active=False)]
        repo.restore_all(**{"id__in": ids})
        all_products: QuerySet[Products] = Products.objects.all()
        f: bool = True
        for tab in all_products:
            if not tab.is_active:
                f: bool = False
        self.assertEqual(f, True)
