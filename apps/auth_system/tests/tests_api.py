# -*- coding: utf-8 -*-
import json

from apps.auth_system.models import Users
from core.tests.IntegrationTest import IntegrationTest


class SecurityTest(IntegrationTest):

    def test_user_can_login(self):
        password_ = {'email': self.user_client.email, "password": "123"}
        response = self.client.post("/api/v1/auth/login/", json.dumps(password_), content_type="application/json")
        json_response = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response["email"], self.user_client.email)

    def test_user_wrong_login(self):
        password_ = {'email': "user@mail.com", "password": "345"}
        response = self.client.post("/api/v1/auth/login/", json.dumps(password_), content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_user_can_register(self):
        user_json = {'email': "login.sr@gmail.com", "password": "123"}
        response = self.client.post("/api/v1/auth/register/", json.dumps(user_json), content_type="application/json")
        response_json = response.data
        self.assertEqual(response.status_code, 200)
        user = Users.objects.get(email=user_json["email"])
        self.assertEqual(user.email, user_json['email'])
        self.assertEqual(response_json['data'], True)

    def test_get_route_without_token(self):
        response = self.client.post("/api/v1/users/")
        self.assertEqual(response.status_code, 401)

    def test_get_route_wrong_token(self):
        header = {'HTTP_AUTHORIZATION': 'Bearer dbjfsdbfj84394thsdk'}
        response = self.client.post("/api/v1/users/", **header, content_type="application/json")
        self.assertEqual(response.status_code, 401)

    def test_get_permission_by_module(self):
        data = {'module': 'products'}
        dumps = json.dumps(data)
        response = self.client.post("/api/v1/auth/get_permission/", dumps, **self.client_token_headers,
                                    content_type="application/json")
        response_json = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['data'], {"view": True})
