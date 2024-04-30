import os
import random
import uuid
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.categories.models import Categories
from core.base.models import Time
from core.misc.utils import validate_char_field


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    new_filename: int = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename: str = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'products/{final_filename}'.format(final_filename=final_filename)



class Products(Time):
    sdk = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nombre", validators=[validate_char_field])
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Categoría")
    category_name = models.CharField(max_length=100, verbose_name="Nombre de Categoría")
    brand = models.CharField(max_length=100, verbose_name="Marca")
    image = models.ImageField(upload_to=upload_file_path, verbose_name='Imágen', blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0.0, verbose_name='Precio',
                                validators=[MinValueValidator(Decimal('0.00'))])
    qty = models.IntegerField(null=True, blank=True, verbose_name="Cantidad")
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name="Descripción",
                                   validators=[validate_char_field])

    class Meta:
        verbose_name: str = "Producto"
        verbose_name_plural: str = "Productos"
        db_table: str = "products"

    def __str__(self):
        return self.name
