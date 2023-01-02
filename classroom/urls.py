from django.urls import path, include
from .views import *
from exam.views import classroom_tests
app_name = 'classroom'

urlpatterns = [
    path('', ClassesDashboard.as_view(), name="homepage"),
    path('classroom/new', create_classroom, name="create_classroom"),
    path('classroom/api/', include("classroom.api.urls")),
    path('classroom/<str:pk>', ClassroomDetail.as_view(), name="classroom_detail"),
    path('classroom/<str:pk>/assignment/new', create_assignment, name="create_assignment"),
    path('classroom/join/<str:pk>', join_classroom, name="join_classroom"),
    # topics
    path('classroom/<str:pk>/topics/<str:topic_id>', topic_posts, name="topic_posts"),
    # posts
    path('classroom/<str:pk>/post', create_post, name="post_to_classroom"),
    path('classroom/post/<str:pk>', PostDetail.as_view(), name="post_detail"),
    path('classroom/post/<str:pk>/edit', edit_post, name="edit_post"),
    path('classroom/post/<str:pk>/delete', delete_post, name="delete_post"),
    # assignment
    path('classroom/<str:pk>/assignments', classroom_assignment, name="view_classroom_assignment"),
    path('classroom/assignment/<str:pk>', view_assignment, name="view_assignment"),
    # students
    path('classroom/<str:pk>/students', classroom_students, name="classroom_students"),
    path('classroom/<str:pk>/groups', classroom_groups, name="classroom_groups"),
    # files
    path('classroom/<str:pk>/files', classroom_files, name="classroom_files"),
    # tests
    path('classroom/<str:pk>/tests', classroom_tests, name="classroom_tests"),
    #weeklies
    path('classroom/<int:cls_pk>/weeklies/', include("weeklies.urls"))
]
   