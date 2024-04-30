from apps.categories.models import Categories

from core.services.Service import Service


class CategoriesInsertService(Service):
    model: type[Categories] = Categories

    def before_create(self, row):
        if row.get('image') == "":
            row['image'] = None
        return row

    def before_update(self, instance, row):
        if row.get('image') == "":
            row['image'] = None
        return row
