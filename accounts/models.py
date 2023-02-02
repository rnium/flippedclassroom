from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from classroom.models import Classroom
from tasks.models import Group, Work
from itertools import chain


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200)
    institutional_id = models.CharField(max_length=200, null=True)
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
        
    @property
    def num_classrooms(self):
        teaching = Classroom.objects.filter(teachers=self.user).count()
        learning = Classroom.objects.filter(students=self.user).count()
        return teaching+learning


    def tasks_score(self, classroom):
        total_score = 0
        group_works = Work.objects.filter(group__members=self.user, task__classroom=classroom)
        indiv_works = Work.objects.filter(group=None, submission_by=self.user, task__classroom=classroom)
        all_works = list(chain(group_works, indiv_works))
        for work in all_works:
            if work.score != None:
                total_score += work.score
            else:
                return None
        return total_score
