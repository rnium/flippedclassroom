from django.contrib import admin
from classroom.models import *

# Register your models here.
admin.site.register(Classroom)
admin.site.register(ClassroomPost)
admin.site.register(PostAttachment)
admin.site.register(Comment)
admin.site.register(Assignment)
admin.site.register(AssignmentAttachment)
admin.site.register(PostTopic)
admin.site.register(AssessmentMeta)
admin.site.register(Assessment)