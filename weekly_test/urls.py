from django.urls import path, include
from weekly_test import views


# test/weeklies
app_name = "weekly_test"

urlpatterns = [
    path('<str:pk>/start', views.take_test, name='take_test'),
    path('<str:pk>/new', views.QuestionCreate.as_view(), name='create_question'),
    path('<str:pk>/questions', views.view_ques, name='view_ques'),
    path('<str:pk>/view', views.view_test, name='view_test'),
    path('<str:pk>/delete', views.delete_test_get, name='delete_test_get'),
    path('answersheet/<str:pk>', views.view_answersheet, name='view_answersheet'),
]