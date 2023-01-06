from unicodedata import name
from django.urls import path
from weeklies.api.views import UpdateWeeklyAV, createWeekly, add_tutorial

# 'classroom/<int:cls_pk>/weeklies/api/' --->

urlpatterns = [
    path('create', createWeekly, name='create_weekly'),
    path('<str:pk>/update', UpdateWeeklyAV.as_view(), name='update_weekly'),
    path('<str:pk>/tutorial/add', add_tutorial, name='add_tutorial')
]
