from typing import Any

from django.urls import path

from ..apis.UsersV1API import List

app_name: str = 'users'

actions: dict[str, str] = {"get": "list", "post": "insert"}
actions_pk: dict[str, str] = {"delete": "delete", "get": "retrieve", "put": "update"}

urlpatterns: list[Any] = [
    # Users
    path('', List.as_view(actions=actions), name='UsersList'),
    path('delete_all/', List.as_view({'post': 'delete_all'}), name='UsersDelete'),
    path('restore/', List.as_view({'post': 'restore'}), name='UsersRestore'),
    path('restore_all/', List.as_view({'post': 'restore_all'}), name='UsersRestoreAll'),
    path('<pk>/', List.as_view(actions=actions_pk), name='UsersPK'),

]
