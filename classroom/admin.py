from django.contrib import admin
from classroom.models import *

# Register your models here.
admin.site.register(Classroom)
admin.site.register(ClassroomPost)
admin.site.register(PostAttachment)
admin.site.register(Comment)