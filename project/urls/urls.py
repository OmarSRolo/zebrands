"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from project.urls.schema import schema_view_v1

urlpatterns = [
    path('api/v1/docs/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('project.urls.v1', namespace='v1')),
    path('admin/', admin.site.urls),
]

# Admin site
admin.site.site_header = "ZebrandsAdmin"
admin.site.index_title = "Panel del administrador"
admin.site.site_title = "ZebrandsAdmin"

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
