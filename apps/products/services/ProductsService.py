from apps.products.models import Products, Track
from core.services.Service import Service


class ProductsService(Service):
    model: type[Products] = Products

    def track_products(self, product_id: int, user_id: str) -> Track:
        assert user_id is not None
        assert product_id is not None
        track, created = Track.objects.update_or_create(product_id=product_id, user=user_id)
        if not created:
            track.total_views += 1
            track.save()
        return track
