import base64
import json
from decimal import Decimal
from typing import Any

from parameterized import parameterized

from apps.categories.models import Categories
from apps.infrastructure.tests.factories import ProductsFactory
from apps.products.models import Products
from core.tests.End2EndTest import End2EndTest


class ProductsAPITest(End2EndTest):
    url: str = "/api/v1/products/"
    fixtures = ['test/users.json', 'products_categories.json', 'products_products.json']

    def setUp(self):
        super(ProductsAPITest, self).setUp()
        self.category_normal = Categories.objects.filter(not_assigned=True, is_deleted=False, is_active=True).first()

    @parameterized.expand(
        [

            (ProductsFactory, True),
            (ProductsFactory, False),
        ]
    )
    def test_create_product(self, factory, with_image: bool):
        product_factory: dict[str, Any] = factory.build()
        product_factory['is_active'] = "true"
        product_factory['category'] = self.category_normal.pk

        if with_image:
            product_factory["image"] = self.create_image()

        product_factory['category'] = self.category_normal.pk
        response = self.client.post("/api/v1/products/", product_factory, **self.super_token_headers)
        product = Products.objects.filter(is_active=True, is_deleted=False).last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(product.name, product_factory['name'])
        self.assertEqual(product.description, product_factory['description'])
        self.assertEqual(product.is_active, True)
        self.assertEqual(product.category_id, product_factory['category'])
        self.assertEqual(product.price, Decimal(product_factory['price']).quantize(Decimal('.01')))
        if with_image:
            self.assertIsNotNone(product.image)

    #
    def test_cant_create_product_without_category(self):
        product = ProductsFactory.create(category="", is_active='true')
        response = self.client.post("/api/v1/products/", product, **self.super_token_headers)
        self.assertEqual(response.status_code, 400)

    def test_can_create_product_no_activated(self):
        product = ProductsFactory.create(is_active='false')
        product['category'] = self.category_normal.pk

        response = self.client.post("/api/v1/products/", product, **self.super_token_headers)
        self.assertEqual(response.status_code, 200)
        product = Products.objects.filter(is_active=False, is_deleted=False).last()
        self.assertFalse(product.is_active)
        self.assertFalse(product.is_deleted)

    def test_can_update_product_no_activated(self):
        product_saved = Products.objects.filter(is_active=True, is_deleted=False).last()
        product: dict[str, Any] = {"is_active": "false", 'category': self.category_normal.pk}
        response = self.client.put(f"/api/v1/products/{product_saved.pk}/", product,
                                   **self.super_token_headers)
        product_saved.refresh_from_db()
        self.assertFalse(product_saved.is_active)
        self.assertFalse(product_saved.is_deleted)
        self.assertEqual(response.status_code, 200)

    def test_get(self):
        product = Products.objects.filter(is_deleted=False, is_active=True).first().pk
        response = self.client.get(self.url + str(product) + "/", **self.super_token_headers,
                                   content_type="application/json")
        json_res = response.data
        self.assertEqual(json_res["data"]["id"], product)
        self.assertEqual(json_res["complete"], True)
        self.assertEqual(response.status_code, 200)

    def test_update(self):
        product = Products.objects.filter(is_deleted=False, is_active=True).first().pk
        response = self.client.put(self.url + f"{product}/",
                                   {"name": "Concha", "price": "7.00", "category": self.category_normal.pk},

                                   **self.super_token_headers)
        self.assertEqual(response.status_code, 200)
        json_res = response.data
        table = json_res["data"]
        self.assertEqual(table["id"], product)
        self.assertEqual(table["name"], "Concha")
        self.assertEqual(table["price"], "7.00")

    def test_list(self):
        data: dict[str, Any] = {"filters": {}, "limit": 10, "offset": 0, "order": "asc", "sort": ["pk"]}
        data_to_send: str = base64.b64encode(json.dumps(data).encode('ascii')).decode('ascii')
        response = self.client.get(self.url + f"?q={data_to_send}", **self.super_token_headers,
                                   content_type="application/json")
        json_res = response.data
        total = Products.objects.filter(category__is_active=True, is_active=True, is_deleted=False).count()
        self.assertEqual(json_res["data"]["total"], total)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_res["data"]["results"]), total)

    def test_api_delete(self):
        product = Products.objects.filter(is_deleted=False, is_active=True).last()
        response = self.client.delete(self.url + f"{product.pk}/", content_type="application/json",
                                      **self.super_token_headers)
        product.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(product.is_active, False)
        self.assertEqual(product.is_deleted, True)
