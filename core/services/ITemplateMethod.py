"""
Trigger methods
"""


class IWebhookTemplate:
    def before_get(self):
        pass

    def after_get(self, row):
        return row

    def before_create(self, row):
        return row

    def after_created(self, row):
        return row

    def before_update(self, instance, row):
        return row

    def after_update(self, row):
        return row

    def before_delete(self, row):
        return row

    def after_delete(self):
        pass

    def before_delete_all(self, queryset):
        return queryset

    def after_delete_all(self):
        pass

    def before_restore(self, row):
        pass

    def after_restore(self):
        pass

    def before_restore_all(self, queryset):
        return queryset

    def after_restore_all(self):
        pass
