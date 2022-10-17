from django.urls import path
from .views import LoginView, SignupView, api_login, api_signup

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login_get"),
    path('api/login', api_login, name="user_login_post"),
    path('signup/', SignupView.as_view(), name="user_signup_get"),
    path('api/signup', api_signup, name="user_signup_post"),
]
   