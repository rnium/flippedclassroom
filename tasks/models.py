from django.db import models
from django.contrib.auth.models import User
from os.path import join, basename
from pathlib import Path
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
    instruction = models.CharField(max_length=1000, null=True, blank=True)
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
    
    @property
    def is_weekly_task(self):
        if self.weekly == None:
            return False
        else:
            return True
        
    @property
    def weekly_section(self):
        if self.is_weekly_task:
            if self.preclass:
                return "PreClass"
            elif self.inclass:
                return "InClass"
            elif self.postclass:
                return "PostClass"
            else:
                return "Weekly General"
        else:
            return "General"


class TaskAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.task.classroom.id), 'tasks', str(self.task.id), filename)

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath, max_length=1000)

    @property
    def filename(self):
        name_str = basename(self.attached_file.name)
        return name_str.replace('_', ' ')
    
    @property
    def css_class(self):
        css_classes = {
            ".pdf": "bx bxs-file-pdf",
            ".pptx":"bx bx-slideshow",
            ".jpg": "bx bxs-file-image",
            ".png": "bx bxs-file-image",
            ".docx": "bx bxs-file-doc",
            ".zip": "bx bxs-file-archive",
            ".txt": "bx bxs-file-txt",
            ".py": "bx bxl-python",
            ".pyw": "bx bxl-python"
        }
        file_extention = Path(self.filename).suffix
        if file_extention in css_classes:
            return css_classes[file_extention]
        else:
            return "bx bxs-file-blank"


class Group(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    
    @property
    def work_submitted(self):
        qs = self.work_set.filter(is_submitted=True)
        return bool(len(qs))
    
    @property
    def work(self):
        qs = self.work_set.all()
        if len(qs) > 0:
            return qs[0]
        else:
            return False

    @property
    def submitted_work(self):
        qs = self.work.filter(is_submitted=True)[0]


class Work(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    submission_by = models.ForeignKey(User, on_delete=models.CASCADE)
    is_submitted = models.BooleanField(default=False)
    group = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    score = models.IntegerField(null=True, blank=True)
    submission_time = models.DateTimeField(null=True, blank=True)
    
    @property
    def is_late(self):
        if self.submission_time > self.task.deadline:
            return True
        else:
            return False
    
    @property
    def attachments(self):
        return self.workattachment_set.all()
    
    @property
    def num_attachments(self):
        return self.attachments.count()
    

class WorkAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.work.task.classroom.id), 'tasks', str(self.work.task.id), 'submissions', filename)

    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath, max_length=1000)

    @property
    def filename(self):
        name_str = basename(self.attached_file.name)
        return name_str.replace('_', ' ')
    
    @property
    def css_class(self):
        css_classes = {
            ".pdf": "bx bxs-file-pdf",
            ".pptx":"bx bx-slideshow",
            ".jpg": "bx bxs-file-image",
            ".png": "bx bxs-file-image",
            ".docx": "bx bxs-file-doc",
            ".zip": "bx bxs-file-archive",
            ".txt": "bx bxs-file-txt",
            ".py": "bx bxl-python",
            ".pyw": "bx bxl-python"
        }
        file_extention = Path(self.filename).suffix
        if file_extention in css_classes:
            return css_classes[file_extention]
        else:
            return "bx bxs-file-blank"