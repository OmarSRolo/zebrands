from django.db import models

from apps.products.models import Products
from core.base.models import Time


class Track(Time):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='traces')
    user = models.UUIDField()
    metadata = models.JSONField(default={})

    class Meta:
        verbose_name: str = "Track Producto"
        verbose_name_plural: str = "Track Productos"
        db_table: str = "track_products"
