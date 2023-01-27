from django.contrib import admin
from weekly_test.models import WeeklyTest, AnswerSheet, Question, McqAnswer, DescriptiveAnswer, McqOption
# Register your models here.
admin.site.register(WeeklyTest)
admin.site.register(AnswerSheet)
admin.site.register(Question)
admin.site.register(McqAnswer)
admin.site.register(DescriptiveAnswer)
admin.site.register(McqOption)