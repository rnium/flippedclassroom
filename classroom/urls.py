from django.urls import path, include
from .views import *
app_name = 'classroom'

urlpatterns = [
    path('', ClassesDashboard.as_view(), name="homepage"),
    path('classroom/api/', include("classroom.api.urls")),
    path('classroom/<str:pk>', ClassroomDetail.as_view(), name="classroom_detail"),
    path('classroom/<str:pk>/post', create_post, name="post_to_classroom"),
    path('classroom/<str:pk>/assignment/new', create_assignment, name="create_assignment"),
    path('classroom/join/<str:pk>', join_classroom, name="join_classroom"),
    path('classroom/post/<str:pk>', PostDetail.as_view(), name="post_detail"),
    path('classroom/post/<str:pk>/edit', UnderDev.as_view(), name="post_edit"),
]
   