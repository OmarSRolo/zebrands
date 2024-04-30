import re

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.serializers import ValidationError


def json_result(status: bool = True, message: str = "", data=None, status_code: int = 200) -> Response:
    if hasattr(data, 'errors'):
        return Response({"complete": status, "message": data.errors, "data": []}, status=400)
    elif not status:
        return Response({"complete": status, "message": "Elemento no encontrado.", "data": []}, status=status_code)
    return Response({"complete": status, "message": message, "data": data}, status=status_code)


def validate_image(image):
    if image:
        file_size = image.size
        if file_size > settings.MAX_IMAGE_SIZE * 1024:
            raise ValidationError({"complete": True, "message": {
                "name": [
                    _('The size of file must be less than %(max_size)s kb') % {'max_size': settings.MAX_IMAGE_SIZE}]}})


def validate_image_one_mb(image):
    if image:
        file_size = image.size
        if file_size > settings.MAX_IMAGE_SIZE * 10240:
            raise ValidationError({"complete": True, "message": {
                "name": [_('The size of file must be less than %(max_size)s kb') % {'max_size': 1000}]}})


def sanitize_input(text: str) -> str:
    # ([^\x00-\x7Fá-úÁ-Ú])+
    return re.sub("[^[\x00-\x7F]|á-ú|Á-Ú]+", "", text)


def validate_char_field(value):
    pattern: str = r'[^\x00-\x7F\u00E2\u00E4\u00E8\u00E9\u00EA\u00EB\u00EE\u00EF\u00F4\u0153\u00F9\u00FB\u00FC\u00FF\u00E7\u00C0\u00C2\u00C4\u00C8\u00C9\u00CA\u00CB\u00CE\u00CF\u00D4\u0152\u00D9\u00DB\u00DC\u0178\u00C7\u00F1\u00D1\u00E1\u00E9\u00ED\u00F3\u00FA\u00C1\u00C9\u00CD\u00D3\u00DA\u00A1\u003F\u00BF]+'
    if re.search(pattern, value):
        raise ValidationError(
            {"complete": True, "message": {"name": [_("There are fields with characters not allowed")]}})
