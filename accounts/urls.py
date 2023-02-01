from django.urls import path
from .views import LoginView, SignupView, LogoutView, api_login, api_signup, set_avatar, view_profile, edit_profile

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login_get"),
    path('api/login', api_login, name="user_login_post"),
    path('logout/', LogoutView.as_view(), name="user_logout"),
    path('signup/', SignupView.as_view(), name="user_signup_get"),
    path('profile/<int:pk>', view_profile, name="view_profile"),
    path('profile/<int:pk>/edit', edit_profile, name="edit_profile"),
    path('api/signup', api_signup, name="user_signup_post"),
    path('profile/avatar/set', set_avatar, name="set_avatar"),
]
   