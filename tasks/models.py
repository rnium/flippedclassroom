from django.db import models
from django.contrib.auth.models import User
from os.path import join, basename
import uuid
from classroom.models import Classroom
from weeklies.models import Weekly


class Task(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    title = models.CharField(max_length=250)
    marks = models.IntegerField(default=100)
    instruction = models.CharField(max_length=1000)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    weekly = models.ForeignKey(Weekly, null=True, blank=True, on_delete=models.SET_NULL)
    preclass = models.BooleanField(default=False)
    inclass = models.BooleanField(default=False)
    postclass = models.BooleanField(default=False)
    addded = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.classroom.name} - Task"

    @property
    def is_group_task(self):
        return bool(self.group_set.count())


class TaskAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.task.classroom.id), 'tasks', str(self.task.id), filename)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))


class Group(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)


class SubmittedWork(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    submission_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField()


class WorkAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.task.classroom.id), 'tasks', str(self.task.id), 'submissions', filename)

    work = models.ForeignKey(SubmittedWork, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    @property
    def filename(self):
        return str(basename(self.attached_file.name))