from django.urls import path
from tasks import views
app_name = 'tasks'

# <included from classroomn.urls> url: classroom/<str:cls_pk>/task/

urlpatterns = [
    path('new', views.create_task, name="create_task"),
    path('<str:pk>', views.TaskDetail.as_view(), name="view_task"),
    path('<str:pk>/upload_work', views.upload_work, name="upload_work"),
    path('work/<str:pk>/changesubmission', views.change_work_submission_status, name="change_work_submission_status"),
]
   