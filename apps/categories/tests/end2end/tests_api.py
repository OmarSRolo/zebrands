import base64
import json

from parameterized import parameterized

from apps.categories.dto.CategoriesDTO import CategoriesDTO
from apps.categories.models.categories import Categories
from apps.categories.services.CategoriesServices import CategoriesService
from apps.infrastructure.factories.factories import CategoriesFactory
from core.tests.IntegrationTest import IntegrationTest


class CategoriesAPITest(IntegrationTest):
    url = "/api/v1/categories/"
    fixtures = ['test/users.json', 'products_categories.json']

    def setUp(self):
        super(CategoriesAPITest, self).setUp()
        self.service = CategoriesService()
        self.serializer = CategoriesDTO

    @parameterized.expand([
        (CategoriesFactory,),
    ])
    def test_insert(self, factory):
        category = factory.build()
        category['image'] = self.create_image()
        category['is_active'] = "true"
        response = self.client.post(self.url, category, **self.super_token_headers)
        self.assertEqual(response.status_code, 200)
        json_res = response.data
        category_returned = json_res["data"]
        category_saved: Categories = Categories.objects.filter(is_active=True, is_deleted=False).last()
        self.assertEqual(category['name'], category_returned['name'])
        self.assertIsNotNone(category_saved.image)
        self.assertEqual(category['name'], category_saved.name)

    def test_get(self):
        caltegory = Categories.objects.filter(is_deleted=False, is_active=True).first().pk
        response = self.client.get(self.url + str(caltegory) + "/", **self.super_token_headers,
                                   content_type="application/json")
        json_res = response.data
        self.assertEqual(json_res["data"]["id"], caltegory)
        self.assertEqual(json_res["complete"], True)
        self.assertEqual(response.status_code, 200)

    def test_client_can_get(self):
        category = Categories.objects.filter(is_deleted=False, is_active=True).first().pk
        response = self.client.get(self.url + str(category) + "/", **self.client_token_headers,
                                   content_type="application/json")
        json_res = response.data
        self.assertEqual(json_res["data"]["id"], category)
        self.assertEqual(json_res["complete"], True)
        self.assertEqual(response.status_code, 200)

    def test_client_cannt_insert(self):
        category = CategoriesFactory.build()
        category['image'] = self.create_image()
        response = self.client.post(self.url, category, **self.client_token_headers)
        self.assertEqual(response.status_code, 403)

    def test_list(self):
        data = base64.b64encode(
            json.dumps({"filters": {}, "limit": 20, "offset": 0, "order": "asc", "sort": ["pk"]}).encode(
                'ascii')).decode('ascii')
        response = self.client.get(self.url + "?q=" + data, **self.super_token_headers,
                                   content_type="application/json")
        json_res = response.data
        total = Categories.objects.filter(is_active=True, is_deleted=False, not_assigned=False).count()
        self.assertEqual(json_res["data"]["total"], total)
        self.assertEqual(response.status_code, 200)

    def test_client_can_list(self):
        data = base64.b64encode(
            json.dumps({"filters": {}, "limit": 20, "offset": 0, "order": "asc", "sort": ["pk"]}).encode(
                'ascii')).decode('ascii')
        response = self.client.get(self.url + "?q=" + data, **self.client_token_headers,
                                   content_type="application/json")
        json_res = response.data
        total = Categories.objects.filter(is_active=True, is_deleted=False, not_assigned=False).count()
        self.assertEqual(json_res["data"]["total"], total)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand([
        ("juan",),
        ("pedro",)
    ])
    def test_update(self, name: str):
        category = Categories.objects.filter(is_active=True, is_deleted=False).last()
        data = {"name": name}
        response = self.client.put(self.url + f"{category.pk}/", data, **self.super_token_headers)
        json_res = response.data
        category = json_res["data"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(category["name"], name)

    @parameterized.expand([
        ("juan",),
    ])
    def test_client_cannt_update(self, name: str):
        category = Categories.objects.filter(is_active=True, is_deleted=False).last()
        data = {"name": name}
        response = self.client.put(self.url + f"{category.pk}/", data, **self.client_token_headers)
        self.assertEqual(response.status_code, 403)

    def test_delete(self):
        category_saved = Categories.objects.filter(is_active=True, is_deleted=False, not_assigned=False).last()
        response = self.client.delete(f"/api/v1/categories/{category_saved.pk}/", **self.super_token_headers,
                                      content_type="application/json")
        self.assertEqual(response.status_code, 200)
        json_res = response.data
        self.assertEqual(json_res["message"], "Categoria Eliminada")
        with self.assertRaises(Categories.DoesNotExist):
            category_saved.refresh_from_db()

    def test_api_delete_all(self):
        all_categories = Categories.objects.filter(is_deleted=False, is_active=True)
        ids = [x.id for x in all_categories]
        loads = {"id__in": ids}
        data_to_send = json.dumps(loads)
        response = self.client.post("/api/v1/categories/delete_all/", data_to_send, content_type="application/json",
                                    **self.super_token_headers)
        self.assertEqual(response.status_code, 200)

    def test_restore(self):
        products = Categories.objects.filter(is_active=False).first()
        products.is_active = False
        products.save()
        self.service.restore_by(**{"id": products.pk})
        products.refresh_from_db()
        self.assertEqual(products.is_active, True)

    def test_restore_all(self):
        repo = self.service.serializer(self.serializer)
        ids = [x.id for x in Categories.objects.filter(is_active=False)]
        repo.restore_all(**{"id__in": ids})
        all_categories = Categories.objects.all()
        f = True
        for tab in all_categories:
            if not tab.is_active:
                f = False
        self.assertEqual(f, True)
