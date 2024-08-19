from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    file_overwrite = False

class PublicMediaStorage(S3Boto3Storage):
    location = 'niceclickllc'
    file_overwrite = False