from django.urls import path, include
from .views import *
app_name = 'classroom'

urlpatterns = [
    path('', ClassesDashboard.as_view(), name="homepage"),
    path('classroom/new', create_classroom, name="create_classroom"),
    path('classroom/api/', include("classroom.api.urls")),
    path('classroom/<str:pk>', ClassroomDetail.as_view(), name="classroom_detail"),
    path('classroom/<str:pk>/connections', ClassroomConnections.as_view(), name="classroom_connections"),
    path('classroom/<str:pk>/assessment/create', create_assessment, name="create_assessment"),
    path('classroom/<str:pk>/assessment', view_assessment, name="view_assessment"),
    path('classroom/<str:cls_pk>/assessment/<int:pk>', view_student_assessment, name="view_student_assessment"),
    path('classroom/<str:pk>/assessment/printf', view_assessment_printf, name="view_assessment_printf"),
    path('classroom/<str:cls_pk>/assessments/download/excel', download_assessment_excel, name="download_assessment_excel"),
    path('classroom/<str:pk>/about', ClassroomAbout.as_view(), name="classroom_about"),
    path('classroom/<str:pk>/assignment/new', create_assignment, name="create_assignment"),
    path('classroom/<str:pk>/edit', edit_classroom, name="edit_classroom"),
    path('classroom/join/<str:cls_code>', join_classroom, name="join_classroom"),
    # topics
    path('classroom/<str:pk>/topics/<str:topic_id>', topic_posts, name="topic_posts"),
    # posts
    path('classroom/<str:pk>/post', create_post, name="post_to_classroom"),
    path('classroom/post/<str:pk>', PostDetail.as_view(), name="post_detail"),
    path('classroom/post/<str:pk>/edit', edit_post, name="edit_post"),
    path('classroom/post/<str:pk>/newfile', uploadPostFile, name="uploadPostFile"),
    path('classroom/post/<str:pk>/delete', delete_post, name="delete_post"),
    # assignment
    path('classroom/<str:pk>/assignments', classroom_assignment, name="view_classroom_assignment"),
    path('classroom/assignment/<str:pk>', view_assignment, name="view_assignment"),
    # students
    path('classroom/<str:pk>/students', classroom_students, name="classroom_students"),
    path('classroom/<str:pk>/groups', classroom_groups, name="classroom_groups"),
    # files
    path('classroom/<str:pk>/files', classroom_files, name="classroom_files"),
    # tasks
    path('classroom/<str:cls_pk>/task/', include("tasks.urls")),
]
   