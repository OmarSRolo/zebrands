from apps.categories.models import Categories
from apps.products.models import Products
from django.db.models import QuerySet
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from core.services.Service import Service


class CategoriesService(Service):
    model: type[Categories] = Categories

    def before_delete_all(self, queryset):
        try:
            not_assigned: Categories = self.model.objects.get(not_assigned=True)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"complete": True, "message": {"name": [_("You must set No Assigned Category")]}})
        for category in queryset:
            products: QuerySet[Products] = Products.objects.filter(category=category)
            for product in products:
                product.category = not_assigned
                product.category_name = not_assigned.name
            Products.objects.bulk_update(products, ['category', 'category_name'])

    def delete_all(self, soft=True, **kwargs):
        objects_filter: QuerySet[Categories] = self.model.objects.filter(**kwargs)
        self.before_delete_all(objects_filter)
        if soft:
            for a in objects_filter:
                if a.not_assigned:
                    continue
                else:
                    a.deleted_at = now()
                    a.is_active = False
                    a.is_available = False
                    a.is_deleted = True
            self.model.objects.bulk_update(objects_filter, ['is_active', 'is_deleted', 'deleted_at', 'available'])
        else:
            for a in objects_filter:
                if not a.not_assigned:
                    a.delete()
        self.after_delete_all()
        return True, 0

    def before_delete(self, row):
        products: QuerySet[Products] = Products.objects.filter(category=row, is_deleted=False, is_active=True)
        try:
            not_assigned: Categories = self.model.objects.get(not_assigned=True, is_deleted=False, is_active=True)
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"complete": True, "message": {"name": [_("You must set No Assigned Category")]}})
        for product in products:
            product.category = not_assigned
            product.category_name = not_assigned.name
        Products.objects.bulk_update(products, ['category', 'category_name'])

    def delete_by(self, soft=True, **kwargs):
        try:
            category_deleted: Categories = self.model.objects.get(pk=kwargs.get("id"))
        except self.model.DoesNotExist:
            raise serializers.ValidationError(
                {"complete": True, "message": {"category": [_("The category sent, It doesn't exist")]}})
        if category_deleted.not_assigned:
            return False, 0
        self.before_delete(category_deleted)

        if soft:
            category_deleted.deleted_at = now()
            category_deleted.is_active = False
            category_deleted.is_available = False
            category_deleted.is_deleted = True
            category_deleted.save()
        else:
            category_deleted.delete()

        return True, 0
