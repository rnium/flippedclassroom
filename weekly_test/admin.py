from django.contrib import admin
from weekly_test.models import WeeklyTest, AnswerSheet, Question
# Register your models here.
admin.site.register(WeeklyTest)
admin.site.register(AnswerSheet)
admin.site.register(Question)