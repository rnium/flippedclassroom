from django.urls import path, include
from exam import views

app_name = "exam"

urlpatterns = [
    path('<str:pk>/start', views.take_test, name='take_test'),
    path('<str:pk>/new', views.QuestionCreate.as_view(), name='create_question'),
    path('<str:pk>/view', views.TestView.as_view(), name='view_test'),
    path('<str:pk>/edit', views.edit_test, name='edit_test'),
    path('answersheet/<str:pk>', views.view_answersheet, name='view_answersheet'),
]