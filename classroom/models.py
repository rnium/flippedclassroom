from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
import uuid
from os.path import join


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to="profiles/dp/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Classroom(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    name = models.CharField(max_length=200)
    description =  models.CharField(max_length=500, null=True, blank=True)
    teachers = models.ManyToManyField(Account, related_name='teacher')
    students = models.ManyToManyField(Account, related_name='student', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.id}"


class ClassroomPost(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    description = models.CharField(max_length=9999)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post of: {self.classroom}"


class PostAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.classroom_post.classroom), filename)

    classroom_post = models.ForeignKey(ClassroomPost, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    