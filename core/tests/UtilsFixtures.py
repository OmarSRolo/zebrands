from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpRequest
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class BaseTest(APITestCase):
    fixtures = ['test/users.json']

    def setUp(self):
        self.request = HttpRequest()
        self.request.META = {"SERVER_NAME": "example.com", "SERVER_PORT": 8000}

        self.create_super_user()
        self.create_user_administrator()
        self.create_user_client()

        self.create_token_user_adminstrator()
        self.create_token_user_client()
        self.create_token_superuser()

        self.create_client_token_headers()
        self.create_administrator_token_headers()
        self.create_super_token_headers()

    def get_group(self, name="Admin"):
        self.group = Group.objects.get(name=name)

    def create_super_token_headers(self):
        self.super_token_headers = {'HTTP_AUTHORIZATION': self.super_token}

    def create_client_token_headers(self):
        self.client_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_client)}

    def create_administrator_token_headers(self):
        self.administrator_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_administrator)}

    def create_token_user_client(self):
        token = AccessToken.for_user(self.user_client)
        token_total = "Bearer {}".format(token)
        self.token_client = token_total

    def create_token_user_adminstrator(self):
        token = AccessToken.for_user(self.user_administrator)
        token_total = "Bearer {}".format(token)
        self.token_administrator = token_total

    def create_token_superuser(self):
        token = AccessToken.for_user(self.super_user)
        token_total = "Bearer {}".format(token)
        self.super_token = token_total

    def create_super_user(self, **kwargs):
        data = {"email": 'admin@mail.com', "password": make_password("123")}
        data.update(kwargs)
        self.super_user = User.objects.create_superuser(**data)

    def create_user_client(self, **kwargs):
        data = {"email": 'client@client.com', "password": make_password("123")}
        data.update(kwargs)
        user_client = User.objects.create(**data)
        self.get_group("Clients")
        user_client.groups.add(self.group)
        self.user_client = user_client

    def create_user_administrator(self, **kwargs):
        data = {"email": 'administrator@administrator.com', "password": make_password("123"), "role": 'Administrador'}
        data.update(kwargs)
        user_administrator = User.objects.create(**data)
        self.get_group()
        user_administrator.groups.add(self.group)
        self.user_administrator = user_administrator

    def create_image(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file = SimpleUploadedFile(name='test_image.jpg', content=small_gif, content_type='image/jpeg')
        return file
