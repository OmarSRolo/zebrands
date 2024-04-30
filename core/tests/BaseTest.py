from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase


class BaseTest(APITestCase):
    multi_db: bool = True
    databases: str = "__all__"

    def create_image(self):
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file = SimpleUploadedFile(name='test_image.jpg', content=small_gif, content_type='image/jpeg')
        return file
