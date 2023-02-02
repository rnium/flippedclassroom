from django.urls import path
from . import views

urlpatterns = [
    path('newclassroom', views.create_classroom, name="create_classroom_api"),
    path('<str:pk>/posts', views.ClassroomPostsView.as_view(), name="classroom_posts"),
    path('<str:pk>/update', views.UpdateClassroomAV.as_view(), name="update_classroom"),
    # path('<str:pk>/edit', views.update_classroom_info, name="update_classroom"),
    path('<str:pk>/removestudent', views.remove_student, name="remove_student"),
    path('post/<str:pk>/postcomment', views.post_comment, name="post_comment"),
    path('post/<str:pk>/update', views.update_post_des_and_rm_files, name="update_post_des_and_rm_files"),
    path('post/<str:pk>/delete', views.delete_post, name="delete_post_api"),
]
   