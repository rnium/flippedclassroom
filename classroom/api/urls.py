from django.urls import path
from . import views

urlpatterns = [
    path('newclassroom', views.create_classroom, name="create_classroom_api"),
    path('<str:pk>/posts', views.ClassroomPostsView.as_view(), name="classroom_posts"),
    path('post/<str:pk>/postcomment', views.post_comment, name="post_comment"),
]
   