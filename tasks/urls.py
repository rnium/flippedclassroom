from django.urls import path
from tasks import views
app_name = 'tasks'

# <included from classroomn.urls> url: classroom/<str:cls_pk>/task/

urlpatterns = [
    path('new', views.create_task, name="create_task"),
]
   