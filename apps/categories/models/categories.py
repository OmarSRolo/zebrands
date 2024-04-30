import os
import random

from django.db import models

from core.base.models import Time
from core.misc.utils import validate_char_field


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_file_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)

    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return 'categories/{final_filename}'.format(final_filename=final_filename)


class Categories(Time):
    name = models.CharField(max_length=100, verbose_name="Nombre", validators=[validate_char_field])
    image = models.ImageField(upload_to=upload_file_path, verbose_name='Imágen', blank=True)
    not_assigned = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = "categories"

    def __str__(self):
        return self.name
