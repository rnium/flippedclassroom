from django.contrib import admin
from tasks.models import Task, TaskAttachment, Group, Work, WorkAttachment
# Register your models here.

admin.site.register(Task)
admin.site.register(TaskAttachment)
admin.site.register(Group)
admin.site.register(Work)
admin.site.register(WorkAttachment)