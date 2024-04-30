# Generated by Django 5.0.4 on 2024-04-30 21:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_products_sdk'),
    ]

    operations = [
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_created=True, auto_now=True, verbose_name='Fecha de actualización')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now_add=True, verbose_name='Fecha de creación')),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='Fecha de eliminación')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Eliminado')),
                ('user', models.UUIDField()),
                ('metadata', models.JSONField(default={})),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traces', to='products.products')),
            ],
            options={
                'verbose_name': 'Track Producto',
                'verbose_name_plural': 'Track Productos',
                'db_table': 'track_products',
            },
        ),
    ]
