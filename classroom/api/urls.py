from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/posts', views.ClassroomPostsView.as_view(), name="homepage"),
    path('post/<str:pk>/postcomment', views.post_comment, name="post_comment"),
]
   