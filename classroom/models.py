from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
import uuid
from os.path import join


class Classroom(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    name = models.CharField(max_length=50)
    course = models.CharField(max_length=20)
    teachers = models.ManyToManyField(User, related_name='teacher')
    students = models.ManyToManyField(User, related_name='student', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.id}"

    @property
    def num_students(self):
        return self.students.count()
    
    @property
    def teacher_name(self):
        teachers = self.teachers.all()
        if len(teachers) > 0:
            teacher1 = teachers[0]
            first_name = teacher1.first_name
            if first_name:
                return first_name
            else:
                return teacher1.username
        else:
            return None

    @property
    def last_post_time(self):
        if self.classroompost_set.count() > 0:
            post = self.classroompost_set.latest('posted')
            return post.posted
        else:
            return False


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
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post id-{self.id} of: {self.classroom}"
    
    @property
    def num_comments(self):
        return self.comment_set.count()

    @property
    def num_attachments(self):
        return self.postattachment_set.count()   


class PostAttachment(models.Model):
    def filepath(self, filename):
        return join("attachments", str(self.classroom_post.classroom), filename)

    classroom_post = models.ForeignKey(ClassroomPost, on_delete=models.CASCADE)
    attached_file = models.FileField(upload_to=filepath)

    
class Comment(models.Model):
    def get_uuid():
        return uuid.uuid4().hex

    id = models.CharField(
        max_length=50,
        primary_key = True,
        default = get_uuid,
        editable = False,
    )
    post = models.ForeignKey(ClassroomPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='reply')
    comment_text = models.CharField(max_length=9999)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment object({self.id}) of post:<{self.post.id}>"

    @property
    def is_thread(self):
        # a thread is a type of comment which has no parent comment (not a reply comment)
        if self.parent is None:
            return True
        else:
            return False

    @property
    def has_replies(self):
        num_replies = self.reply.count()
        if num_replies > 0:
            return True
        else:
            return False