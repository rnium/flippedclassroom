from optparse import Option
from django.contrib import admin
from .models import *

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(McqOption)
admin.site.register(AnswerSheet)
admin.site.register(McqAnswer)
admin.site.register(DescriptiveAnswer)
# Register your models here.
