from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to="profiles/dp/", null=True, blank=True)

    def __str__(self):
        return self.user.username
    
    @property
    def user_first_name(self):
        first_name = self.user.first_name
        if first_name:
            return first_name
        else:
            return self.user.username
    
    @property
    def user_full_name(self):
        first_name = self.user.first_name
        last_name = self.user.last_name
        if first_name or last_name:
            if first_name and last_name:
                return f"{first_name} {last_name}"
            elif first_name:
                return first_name
            elif last_name:
                return last_name
        else:
            return self.user.username

    @property
    def avatar_url(self):
        if bool(self.profile_picture):
            return self.profile_picture.url
        else:
            return static('accounts/images/blank-dp.svg')
            