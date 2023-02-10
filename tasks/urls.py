from django.urls import path
from tasks import views
app_name = 'tasks'

# <included from classroomn.urls> url: classroom/<str:cls_pk>/task/

urlpatterns = [
    path('new', views.create_task, name="create_task"),
    path('<str:pk>', views.TaskDetail.as_view(), name="view_task"),
    path('<str:pk>/delete', views.delete_task_get, name="delete_task_get"),
    path('<str:pk>/api/delete', views.delete_task, name="delete_task_api"),
    path('files/<int:pk>', views.view_task_file, name="view_task_file"),
    path('work/<str:pk>', views.WorkDetail.as_view(), name="view_work"),
    path('<str:pk>/upload_work', views.upload_work, name="upload_work"),
    path('work/files/<int:pk>', views.view_work_file, name="view_work_file"),
    path('work/<str:pk>/changesubmission', views.change_work_submission_status, name="change_work_submission_status"),
    path('work/<str:pk>/delete', views.delete_work, name="delete_work"),
    path('work/<str:pk>/marking', views.update_work_score, name="update_work_score"),
]
   