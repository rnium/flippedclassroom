from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import User
from django.templatetags.static import static
from classroom.models import Classroom
from tasks.models import Group, Work
from weekly_test.models import AnswerSheet, WeeklyTest
from itertools import chain


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=200, null=True, blank=True)
    institutional_id = models.CharField(max_length=200, null=True, blank=True)
    is_student = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)
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

    
    def group_works(self, classroom):
        gw = Work.objects.filter(group__members=self.user, task__classroom=classroom)
        return gw
    
    def pre_class_works(self, classroom):
        works = Work.objects.filter( Q(group__members=self.user) | Q(group=None, submission_by=self.user), task__classroom=classroom)
        return works
    
    def pre_class_test_answersheets(self, classroom):
        sheets = AnswerSheet.objects.filter(user=self.user, test__weekly__classroom=classroom, test__preclass=True)
        return sheets
    
    
    def classroom_test_answersheets(self, classroom):
        sheets = AnswerSheet.objects.filter(user=self.user, test__weekly__classroom=classroom)
        return sheets
    
    def classroom_unsubmitted_tests(self, classroom):
        timenow = timezone.now()
        qs =  WeeklyTest.objects.filter(weekly__classroom=classroom, answersheet__user=self.user, expiration__gte=timenow, answersheet__submit_time=None)
        return qs
    
    
    def indiv_works(self, classroom):
        iw = Work.objects.filter(group=None, submission_by=self.user, task__classroom=classroom)
        return iw


    def group_task_total_points(self, classroom):
        gw_points = 0
        gw = self.group_works(classroom)
        for work in gw:
            if work.score != None:
                gw_points += work.score
            else:
                return None
        return gw_points
    
    def indiv_task_total_points(self, classroom):
        iw_points = 0
        iw = self.indiv_works(classroom)
        for work in iw:
            if work.score != None:
                iw_points += work.score
            else:
                return None
        return iw_points

    def classroom_test_points(self, classroom):
        points = 0
        sheets = self.classroom_test_answersheets(classroom)
        for sheet in sheets:
            if sheet.total_score != None:
                points += sheet.get_score
            else:
                return None
        return points
    
    def pre_class_points(self, classroom):
        total_points = 0
        works = self.pre_class_works(classroom)
        for work in works:
            if work.score != None:
                total_points += work.score
            else:
                return None
        for test_sheet in self.pre_class_test_answersheets:
            points = test_sheet.total_score
            if points != None:
                total_points += work.score
            else:
                return None
        return total_points