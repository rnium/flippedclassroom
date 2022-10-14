from unicodedata import name
from django.urls import path, include
from . import views

urlpatterns = [
    path('createtest/', views.create_test, name='create_test'),
    path('issue/', views.issue_answer_sheet, name='issue_answer_sheet')
]