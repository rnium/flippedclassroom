from django.urls import path, include
from . import views

app_name = "exam_api"

urlpatterns = [
    path('<str:pk>/create/', views.create_test, name='create_test'),
    path('expiration/update', views.change_test_expiration_status, name='expiration_update'),
    path('issue/', views.issue_answer_sheet, name='issue_answer_sheet'),
    path('<str:pk>/answersheets', views.TestAnswersheetsView.as_view(), name='test_answersheets')
]