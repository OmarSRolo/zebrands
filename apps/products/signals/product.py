from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.auth_system.models import Users
from apps.infrastructure.services.notifications import NotificationService
from apps.products.models import Products


@receiver(post_save, sender=Products)
def product_changed(sender, instance: Products, created, **kwargs):
    if not created:
        all_admin_user: list[str] = Users.objects.filter(groups__name="Admin", is_active=True,
                                                         is_deleted=True).values_list("email")
        NotificationService.send_notification(all_admin_user, instance)
