from django.db import models

from apps.products.models import Products
from core.base.models import Time


class Track(Time):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='traces')
    user = models.UUIDField()
    total_views = models.IntegerField(default=1)
    metadata = models.JSONField(default=dict)

    class Meta:
        verbose_name: str = "Track Producto"
        verbose_name_plural: str = "Track Productos"
        db_table: str = "track_products"
