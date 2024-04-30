from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location: str = 'static'
    default_acl: str = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location: str = 'media'
    default_acl: str = 'public-read'
    file_overwrite: bool = False
