from django.urls import path

from apps.categories.apis.V1ActionsAPI import V1ActionsAPI
from apps.categories.apis.V1CategoriesAPI import List

app_name = 'categories'

actions = {"get": "list", "post": "insert"}
actions_pk = {"delete": "delete", "get": "retrieve", "put": "update"}

urlpatterns = [
    # Categories
    path('', List.as_view(actions=actions), name='CategoriesList'),
    path('delete_all/', V1ActionsAPI.as_view({'post': 'delete_all'}), name='CategoriesDelete'),
    path('restore/', V1ActionsAPI.as_view({'post': 'restore'}), name='CategoriesRestore'),
    path('restore_all/', V1ActionsAPI.as_view({'post': 'restore_all'}), name='CategoriesRestoreAll'),
    path('<pk>/', List.as_view(actions=actions_pk), name='CategoriesPK'),

]
