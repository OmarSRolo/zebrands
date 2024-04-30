from typing import Any

from django.urls import path

from apps.products.apis.V1ActionsAPI import V1ActionsAPI
from apps.products.apis.V1ProductsAPI import List

app_name: str = 'products'

actions: dict[str, str] = {"get": "list", "post": "insert"}
actions_pk: dict[str, str] = {"delete": "delete", "get": "retrieve", "put": "update"}

urlpatterns: list[Any] = [

    path('', List.as_view(actions=actions), name='ProductsList'),

    path('delete_all/', V1ActionsAPI.as_view({'post': 'delete_all'}), name='ProductsDelete'),

    path('<pk>/', List.as_view(actions=actions_pk), name='ProductsPK'),

]
