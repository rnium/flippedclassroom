from django.urls import path, include
from . import views


# test/api/weeklies
app_name = "weekly_test_api"

urlpatterns = [
    path('<str:pk>/create/', views.create_test, name='create_test'),
    path('<str:pk>/delete/', views.delete_test, name='delete_test'),
    path('issue/', views.issue_answer_sheet, name='issue_answer_sheet'),
    path('livestats/<cls_pk>', views.live_test_stats, name='live_test_stats'),
    path('<str:pk>/answersheets', views.TestAnswersheetsView.as_view(), name='test_answersheets'),
    path('answersheet/<str:answersheet_pk>/updatescore', views.update_score, name='update_score')
]