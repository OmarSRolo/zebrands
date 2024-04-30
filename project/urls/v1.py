from django.urls import path, include

app_name: str = 'v1'

urlpatterns = [
    path('auth/', include('apps.auth_system.urls.v1', namespace='v1_auth_system')),
    # path('products/', include('apps.products.urls.v1', namespace='v1_products')),
    # path('categories/', include('apps.categories.urls.v1', namespace='v1_categories')),
    path('users/', include('apps.users.urls.v1', namespace='v1_users')),

]
