from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to="profiles/dp/", null=True, blank=True)

    def __str__(self):
        return self.user.username
