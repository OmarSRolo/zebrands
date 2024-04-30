from django.contrib.auth.models import Group
from parameterized import parameterized
from rest_framework import serializers

from core.tests.IntegrationTest import IntegrationTest
from apps.auth_system.models import Users
from apps.infrastructure.tests.factories import UsersFactory
from apps.users.dto.UsersDTO import UsersDTO, ReadUsersDTO
from apps.users.services.UsersService import UsersService


class UsersTest(IntegrationTest):
    fixtures = ['test/users.json', "users_users.json"]

    def setUp(self):
        super(UsersTest, self).setUp()
        self.repo = UsersService()
        self.serializer = ReadUsersDTO
        self.insert_serializer = UsersDTO

    @parameterized.expand(
        [
            (UsersFactory, "test@test.com"),
        ]
    )
    def test_create_user(self, user, email):
        repo = self.repo.serializer(self.insert_serializer)
        role_id = Group.objects.first().pk
        user_dict = user.create(email=email, role_id=role_id)
        user: Users = repo.insert(**user_dict, return_object=True)
        self.assertEqual(user.email, email)
        user_group = user.groups.first()
        self.assertEqual(user_group.pk, 1)

    @parameterized.expand(
        [
            (UsersFactory,),
        ]
    )
    def test_can_not_create_user_with_same_email(self, user):
        repo = self.repo.serializer(self.insert_serializer)
        user_dict = user.create(email='chicomtz.sr@gmail.com')
        with self.assertRaises(serializers.ValidationError):
            repo.insert(**user_dict)

    def test_get(self):
        repo = self.repo.serializer(self.serializer)
        user = Users.objects.filter(is_active=True, is_deleted=False).last()
        res = repo.find_by(id=user.pk, return_object=True)
        self.assertEqual(res.id, user.pk)
        self.assertEqual(res.email, user.email)

    def test_list(self):
        total = Users.objects.filter(is_active=True, is_deleted=False).count()
        data = {"filters": {}, "limit": 1, "offset": 0, "order": "asc", "sort": ["pk"]}
        repo = self.repo.serializer(self.serializer)
        repo.find_all(**data)
        info = repo.paginate(limit=data.get("limit"), offset=data.get("offset"))
        self.assertEqual(total, info[1])
        self.assertEqual(len(info[0]), data["limit"])

    def test_delete(self):
        repo = self.repo.serializer(self.serializer)
        user = Users.objects.filter(is_active=True, is_deleted=False).last()
        repo.delete_by(**{"id": user.pk})
        user.refresh_from_db()
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_deleted, True)

    def test_update(self):
        repo = self.repo.serializer(self.insert_serializer)
        user = Users.objects.filter(is_active=True, is_deleted=False).last()
        g = Group.objects.last()
        repo.update_by(return_object=True, **{"id": user.pk, "email": "amar@aaa.com", "role_id": g.pk})
        user.refresh_from_db()
        self.assertEqual(user.email, "amar@aaa.com")

    def test_delete_all(self):
        repo = self.repo.serializer(self.serializer)
        ids = [x.id for x in Users.objects.filter(is_active=True, is_deleted=False)]
        repo.delete_all(**{"id__in": ids})
        all_users = Users.objects.filter(is_active=True, is_deleted=False)
        f = True
        for tab in all_users:
            if tab.is_active:
                f = False
        self.assertEqual(f, True)

    def test_restore(self):
        user: Users = Users.objects.filter(is_active=False, is_deleted=False).first()
        user.is_active = False
        user.save()
        self.repo.restore_by(**{"id": user.pk})
        user.refresh_from_db()
        self.assertEqual(user.is_active, True)

    def test_restore_all(self):
        ids = [x.id for x in Users.objects.filter(is_active=False, is_deleted=False)]
        self.repo.restore_all(**{"id__in": ids})
        all_users = Users.objects.filter(is_active=True, is_deleted=False)
        f = True
        for tab in all_users:
            if not tab.is_active:
                f = False
        self.assertEqual(f, True)
