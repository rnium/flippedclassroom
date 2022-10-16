from django.urls import path
from .views import *
app_name = 'classroom'

urlpatterns = [
    path('', home, name="homepage"),
]
   