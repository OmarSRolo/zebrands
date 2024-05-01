from django.conf import settings

from apps.products.models import Products
from cronjobs.tasks import send_email


class NotificationService:
    @staticmethod
    def send_notification(list_emails: list[str], product: Products):
        from_email: str = settings.DEFAULT_FROM_EMAIL
        for user_email in list_emails:
            send_data: dict[str, str] = {"from_email": from_email, "to_email": user_email, "subject": "Product Updated",
                                         "template": "emails/products.html", "message": "Product Updated",
                                         "context": {"product": product.pk, "name": product.name,
                                                     "price": product.price, "sku": product.sku, }}
            send_email.delay(send_data)
