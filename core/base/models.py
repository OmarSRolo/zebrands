from django.db import models


class Time(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, auto_created=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, auto_created=True, verbose_name="Fecha de actualización")
    deleted_at = models.DateTimeField(verbose_name="Fecha de eliminación", blank=True, null=True, editable=False)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_deleted = models.BooleanField(default=False, verbose_name="Eliminado")

    class Meta:
        abstract: bool = True
