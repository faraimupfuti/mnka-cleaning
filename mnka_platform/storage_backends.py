"""
S3-compatible storage backends, used only when USE_S3=True (see settings.py).

PublicMediaStorage  - profile photos etc. Publicly readable, long cache.
PrivateMediaStorage - cleaner ID documents. Never public; every .url call
                       generates a short-lived signed URL, so a link is only
                       ever useful for about an hour and only to someone
                       Django has already authorized (e.g. staff in admin).
"""

from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = "media/public"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = False


class PrivateMediaStorage(S3Boto3Storage):
    location = "media/private"
    default_acl = "private"
    file_overwrite = False
    querystring_auth = True
    querystring_expire = 3600  # signed URLs expire after 1 hour
