from apps.products.models import Products

from core.services.Service import Service


class ProductsService(Service):
    model: type[Products] = Products
