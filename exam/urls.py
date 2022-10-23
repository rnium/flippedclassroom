from django.urls import path, include
from exam import views

app_name = "exam"

urlpatterns = [
    path('', views.TestsHome.as_view(), name='homepage'),
    path('start/<str:pk>/', views.take_test, name='take_test'),
    path('submit/<str:pk>/', views.answer_submit, name='answer_submit'),
    path('<str:pk>/new', views.QuestionCreate.as_view(), name='create_question'),
]