from django.urls import path, include
from . import views


# test/api/weeklies
app_name = "weekly_test_api"

urlpatterns = [
    path('<str:pk>/create/', views.create_test, name='create_test'),
    path('issue/', views.issue_answer_sheet, name='issue_answer_sheet'),
    path('answersheet/<str:answersheet_pk>/updatescore', views.update_score, name='update_score')
]