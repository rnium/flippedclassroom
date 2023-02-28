from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from classroom.models import Classroom
import uuid
from os.path import join, basename
from pathlib import Path


class Weekly(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    weeknum = models.IntegerField()
    topic = models.CharField(max_length=100, blank=True, null=True)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    pre_class_instruction = models.CharField(max_length=2000, blank=True, null=True)
    in_class_instruction = models.CharField(max_length=2000, blank=True, null=True)
    post_class_instruction = models.CharField(max_length=2000, blank=True, null=True)

    def __str__(self):
        return f"{self.classroom.id} - week{self.weeknum}"
    # files properties
    @property
    def preClassFiles(self):
        qs = self.preclassfile_set.all()
        return qs
    
    @property
    def inClassFiles(self):
        qs = self.inclassfile_set.all()
        return qs
    
    @property
    def postClassFiles(self):
        qs = self.postclassfile_set.all()
        return qs
    
    @property
    def hasPreClassFiles(self):
        return bool(len(self.preClassFiles))
    
    @property
    def hasInClassFiles(self):
        return bool(len(self.inClassFiles))
    
    @property
    def hasPostClassFiles(self):
        return bool(len(self.postClassFiles))

    # tutorial properties
     
    @property
    def preClassTuto(self):
        qs = self.preclasstutorial_set.all().order_by('added')
        return qs

    @property
    def inClassTuto(self):
        qs = self.inclasstutorial_set.all().order_by('added')
        return qs

    @property
    def postClassTuto(self):
        qs = self.postclasstutorial_set.all().order_by('added')
        return qs
    
    @property
    def hasPreClassTuto(self):
        qs = self.preclasstutorial_set.all().order_by('added')
        return bool(len(qs))
    
    @property
    def hasInClassTuto(self):
        qs = self.inclasstutorial_set.all().order_by('added')
        return bool(len(qs))
    
    @property
    def hasPostClassTuto(self):
        qs = self.postclasstutorial_set.all().order_by('added')
        return bool(len(qs))

    # tests
    @property
    def preClassUpcomingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(preclass=True, schedule__gt=timenow).order_by('schedule')
    
    @property
    def preClassOngoingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(preclass=True, schedule__lte=timenow, expiration__gt=timenow).order_by('schedule')
    
    @property
    def preClassPreviousTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(preclass=True, expiration__lt=timenow).order_by('schedule')
    
    @property
    def has_pre_class_tests(self):
        return bool(len(self.preClassUpcomingTest) + len(self.preClassPreviousTest))
    
    @property
    def has_pre_class_ongoing_test(self):
        return bool(len(self.preClassOngoingTest))
    
    # in class tests
    @property
    def inClassUpcomingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(inclass=True, schedule__gt=timenow).order_by('schedule')
    
    @property
    def inClassOngoingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(inclass=True, schedule__lte=timenow, expiration__gt=timenow).order_by('schedule')
    
    @property
    def inClassPreviousTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(inclass=True, expiration__lt=timenow).order_by('schedule')
    
    @property
    def has_in_class_tests(self):
        return bool(len(self.inClassUpcomingTest) + len(self.inClassPreviousTest))
    
    @property
    def has_in_class_ongoing_test(self):
        return bool(len(self.inClassOngoingTest))
    
    # post class tests
    @property
    def postClassUpcomingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(postclass=True, schedule__gt=timenow).order_by('schedule')
    
    @property
    def postClassOngoingTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(postclass=True, schedule__lte=timenow, expiration__gt=timenow).order_by('schedule')
    
    @property
    def postClassPreviousTest(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(postclass=True, expiration__lt=timenow).order_by('schedule')
    
    @property
    def has_post_class_tests(self):
        return bool(len(self.postClassUpcomingTest) + len(self.postClassPreviousTest))
    
    @property
    def has_post_class_ongoing_test(self):
        return bool(len(self.postClassOngoingTest))
    
    # forum post
    @property
    def forum_posts(self):
        return self.forumpost_set.all().order_by('added')
    
    @property
    def has_forum_post(self):
        return bool(len(self.forum_posts))
    
    # assigned tasks
    # pre-class task
    @property
    def preClassOngoingTask(self):
        timenow = timezone.now()
        return self.task_set.filter(preclass=True, deadline__gte=timenow).order_by('deadline')
    
    @property
    def preClassPreviousTask(self):
        timenow = timezone.now()
        return self.task_set.filter(preclass=True, deadline__lt=timenow).order_by('deadline')
    
    @property
    def has_pre_class_tasks(self):
        return bool(len(self.preClassOngoingTask) + len(self.preClassPreviousTask))
    
    @property
    def has_pre_class_ongoing_task(self):
        return bool(len(self.preClassOngoingTask))
    # in-class task
    @property
    def inClassOngoingTask(self):
        timenow = timezone.now()
        return self.task_set.filter(inclass=True, deadline__gte=timenow).order_by('deadline')
    
    @property
    def inClassPreviousTask(self):
        timenow = timezone.now()
        return self.task_set.filter(inclass=True, deadline__lt=timenow).order_by('deadline')
    
    @property
    def has_in_class_tasks(self):
        return bool(len(self.inClassOngoingTask) + len(self.inClassPreviousTask))
    
    @property
    def has_in_class_ongoing_task(self):
        return bool(len(self.inClassOngoingTask))
    # post-class task
    @property
    def postClassOngoingTask(self):
        timenow = timezone.now()
        return self.task_set.filter(postclass=True, deadline__gte=timenow).order_by('deadline')
    
    @property
    def postClassPreviousTask(self):
        timenow = timezone.now()
        return self.task_set.filter(postclass=True, deadline__lt=timenow).order_by('deadline')
    
    @property
    def has_post_class_tasks(self):
        return bool(len(self.postClassOngoingTask) + len(self.postClassPreviousTask))
    
    @property
    def has_post_class_ongoing_task(self):
        return bool(len(self.postClassOngoingTask))
    
    @property
    def tests(self):
        return self.weeklytest_set.all()
    
    @property
    def num_tests(self):
        return self.tests.count()
    
    @property
    def tests_total_marks(self):
        total_marks = sum([test.total_marks for test in self.tests])
        return total_marks
    
    @property
    def all_upcoming_tests(self):
        timenow = timezone.now()
        up_tests = self.weeklytest_set.filter(schedule__gt=timenow)
        return up_tests
    
    @property
    def all_prev_tests(self):
        timenow = timezone.now()
        prev_tests = self.weeklytest_set.filter(expiration__lt=timenow)
        return prev_tests
    
    @property
    def ongoing_test(self):
        timenow = timezone.now()
        return self.weeklytest_set.filter(schedule__lte=timenow, expiration__gt=timenow)
    
    # sections total marks
    @property
    def pre_cls_marks(self):
        ongoing_tasks = self.preClassOngoingTask
        prev_tasks = self.preClassPreviousTask
        ongoing_tests = self.preClassOngoingTest
        prev_tests = self.preClassOngoingTest
        total_marks = 0
        for on_task in ongoing_tasks:
            total_marks += on_task.marks
        for prev_task in prev_tasks:
            total_marks += prev_task.marks
        for on_test in ongoing_tests:
            total_marks += on_test.total_marks
        for prev_test in prev_tests:
            total_marks += prev_test.total_marks
        return total_marks
        
    
     
class PreClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'preclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    must_study = models.BooleanField(default=False)
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


class InClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'inclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    must_study = models.BooleanField(default=False)
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
    

class PostClassFile(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.weekly.classroom.id), 'weekly', str(self.weekly.id), 'inclass', filename)

    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    must_study = models.BooleanField(default=False)
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


class PreClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=20) # yt_id = YouTube ID
    description = models.CharField(max_length=1000, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    
    @property
    def yt_url(self):
        url = f"https://www.youtube.com/watch?v={self.yt_id}"
        return url


class InClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=20)
    description = models.CharField(max_length=1000, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    
    @property
    def yt_url(self):
        url = f"https://www.youtube.com/watch?v={self.yt_id}"
        return url


class PostClassTutorial(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    yt_id = models.CharField(max_length=20)
    description = models.CharField(max_length=1000, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)

    @property
    def yt_url(self):
        url = f"https://www.youtube.com/watch?v={self.yt_id}"
        return url

class Forumpost(models.Model):
    weekly = models.ForeignKey(Weekly, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postcontent = models.TextField()
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
