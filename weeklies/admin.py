from django.contrib import admin
from weeklies.models import Weekly, PreClassFile, InClassFile, PostClassFile, PreClassTutorial, InClassTutorial, PostClassTutorial
# Register your models here.

admin.site.register(Weekly)
admin.site.register(PreClassFile)
admin.site.register(InClassFile)
admin.site.register(PostClassFile)
admin.site.register(PreClassTutorial)
admin.site.register(InClassTutorial)
admin.site.register(PostClassTutorial)