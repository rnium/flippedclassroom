from django.db import models
from classroom.models import Classroom
import uuid
from os.path import join, basename



class Weekly(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    weeknum = models.IntegerField(unique=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    pre_class_instruction = models.CharField(max_length=2000, blank=True, null=True)
    in_class_instruction = models.CharField(max_length=2000, blank=True, null=True)
    post_class_instruction = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"{self.classroom.id} - week{self.weeknum}"


class PreClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'preclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath, max_length=1000)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))


class InClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'inclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath, max_length=1000)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))


class PostClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'inclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath, max_length=1000)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))


class PreClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=10) # yt_id = YouTube ID
    description = models.CharField(max_length=1000, blank=True, null=True)


class InClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=10)
    description = models.CharField(max_length=1000, blank=True, null=True)


class PostClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=10)
    description = models.CharField(max_length=1000, blank=True, null=True)