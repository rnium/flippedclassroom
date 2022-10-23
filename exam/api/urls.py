from django.urls import path, include
from . import views

app_name = "exam_api"

urlpatterns = [
    path('<str:pk>/create/', views.create_test, name='create_test'),
    path('issue/', views.issue_answer_sheet, name='issue_answer_sheet')
]