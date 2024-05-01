# from parameterized import parameterized
#
# from core.factories.IntegrationTest import IntegrationTest
# from apps.categories.dto.CategoriesDTO import CategoriesDTO
# from apps.categories.models import Categories
# from apps.categories.services.CategoriesServices import CategoriesService
#
#
# class CategoriesTest(IntegrationTest):
#     fixtures = ['test/users.json', 'products_categories.json']
#
#     def setUp(self):
#         super(CategoriesTest, self).setUp()
#         self.service = CategoriesService()
#         self.serializer = CategoriesDTO
#
#     @parameterized.expand([
#         ({"filters": {}, "limit": 1, "offset": 0, "order": "asc", "sort": ["pk"]}, False,),
#         ({"filters": {}, "limit": 2, "offset": 0, "order": "desc", "sort": ["pk"]}, True,)
#     ])
#     def test_list(self, data, show_actives_values: bool):
#         if show_actives_values:
#             total = Categories.objects.filter(is_active=True, is_deleted=False).count()
#         else:
#             total = Categories.objects.filter(is_deleted=False).count()
#
#         repo = self.service.serializer(self.serializer, **{"request": self.request})
#         repo.find_all(**data, show_actives=show_actives_values)
#         info = repo.paginate(limit=data["limit"], offset=data["offset"])
#         self.assertEqual(total, info[1])
#         self.assertEqual(len(info[0]), data["limit"])
#
#     # SECTION GET
#     def test_get_category(self):
#         self.service.serializer(CategoriesDTO, **{"request": self.request})
#         category = Categories.objects.filter(is_active=True, is_deleted=False).last()
#         res = self.service.find_by(id=category.pk)
#         self.assertEqual(res["id"], category.pk)
#         self.assertEqual(res["name"], category.name)
