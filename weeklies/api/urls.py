from unicodedata import name
from django.urls import path
from weeklies.api.views import createWeekly
# 'classroom/<int:cls_pk>/weeklies/api/' --->

urlpatterns = [
    path('create', createWeekly, name='create_weekly'),
]
