from django.urls import path, include
from weekly_test import views


# test/weeklies
app_name = "weekly_test"

urlpatterns = [
    path('<str:pk>/start', views.take_test, name='take_test'),
    path('<str:pk>/new', views.QuestionCreate.as_view(), name='create_question'),
    path('<str:pk>/view', views.view_test, name='view_test'),
    path('<str:pk>/edit', views.edit_test, name='edit_test'),
    path('answersheet/<str:pk>', views.AnswersheetView.as_view(), name='view_answersheet'),
]