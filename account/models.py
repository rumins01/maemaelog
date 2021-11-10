from django.db import models
from django.contrib.auth.models import User


def get_upload_path(instance, filename):
    return f"/assets/image/profile/"


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=32)
    bio = models.TextField()
    profile_image = models.ImageField(
        upload_to="assets/image/profile/",
        blank=True,
        null=True
    )
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    sex = models.CharField(max_length=8, blank=True, null=True)
