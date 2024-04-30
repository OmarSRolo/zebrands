from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.http import HttpRequest
from rest_framework_simplejwt.tokens import AccessToken

from apps.auth_system.models import Users

User = get_user_model()


class UtilFixture:

    def setUp(self):
        self.request = HttpRequest()
        self.request.META = {"SERVER_NAME": "example.com", "SERVER_PORT": 8000}

        self.user = Users.objects.filter(is_staff=False).first()

        self.create_super_user()
        self.create_user_administrator()
        self.create_user_dependiente()
        self.create_user_client()

        self.create_token_user_adminstrator()
        self.create_token_user_dependiente()
        self.create_token_user_client()
        self.create_token_superuser()
        self.create_token_user()

        self.create_site_and_user_token_headers()
        self.create_site_and_client_token_headers()
        self.create_site_and_dependiente_token_headers()
        self.create_site_and_administrator_token_headers()
        self.create_site_and_super_token_headers()

    def get_group(self, name="Administrador"):
        self.group = Group.objects.get(name=name)

    def create_site_and_super_token_headers(self):
        self.super_token_headers = {'HTTP_AUTHORIZATION': self.super_token}

    def create_site_and_user_token_headers(self):
        self.user_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_user)}

    def create_site_and_client_token_headers(self):
        self.client_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_client)}

    def create_site_and_administrator_token_headers(self):
        self.administrator_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_administrator)}

    def create_site_and_dependiente_token_headers(self):
        self.dependiente_token_headers = {'HTTP_AUTHORIZATION': '{}'.format(self.token_dependiente)}

    def create_token_user(self):
        token = AccessToken.for_user(self.user)
        token_total = "Bearer {}".format(token)
        self.token_user = token_total

    def create_token_user_client(self):
        token = AccessToken.for_user(self.user)
        token_total = "Bearer {}".format(token)
        self.token_client = token_total

    def create_token_user_adminstrator(self):
        token = AccessToken.for_user(self.user_administrator)
        token_total = "Bearer {}".format(token)
        self.token_administrator = token_total

    def create_token_user_dependiente(self):
        token = AccessToken.for_user(self.user_dependiente)
        token_total = "Bearer {}".format(token)
        self.token_dependiente = token_total

    def create_token_superuser(self):
        token = AccessToken.for_user(self.super_user)
        token_total = "Bearer {}".format(token)
        self.super_token = token_total

    def create_super_user(self, **kwargs):
        data = {"email": 'admin@mail.com', "password": '123'}
        data.update(kwargs)
        self.super_user = User.objects.create_superuser(**data)

    def create_user_client(self, **kwargs):
        data = {"email": 'client@client.com', "password": '123', "point": 10}
        data.update(kwargs)
        user_client = User.objects.create(**data)
        self.get_group("Clientes")
        user_client.groups.add(self.group)
        self.user_client = user_client

    def create_user_administrator(self, **kwargs):
        data = {"email": 'administrator@administrator.com', "password": '123', "role": 'Administrador'}
        data.update(kwargs)
        user_administrator = User.objects.create(**data)
        self.get_group()
        user_administrator.groups.add(self.group)
        self.user_administrator = user_administrator

    def create_user_dependiente(self, **kwargs):
        data = {"email": 'dependiente@dependiente.com', "password": '123', "role": 'dependiente'}
        data.update(kwargs)
        user_dependiente = User.objects.create(**data)
        self.get_group('dependiente')
        user_dependiente.groups.add(self.group)
        self.user_dependiente = user_dependiente
