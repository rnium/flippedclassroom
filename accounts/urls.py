from django.urls import path
from .views import LoginView, SignupView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login_get"),
    path('signup/', SignupView.as_view(), name="user_signup_get"),
]
   