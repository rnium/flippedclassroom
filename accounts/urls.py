from django.urls import path
from .views import (LoginView, SignupView, LogoutView, 
                    api_login, api_signup, set_avatar, view_profile, 
                    edit_profile, update_profile, update_password_get, update_password_api, verify_user)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login_get"),
    path('api/login', api_login, name="user_login_post"),
    path('logout/', LogoutView.as_view(), name="user_logout"),
    path('signup/', SignupView.as_view(), name="user_signup_get"),
    path('verify/<uidb64>/<token>', verify_user, name="verify_user"),
    path('profile/<int:pk>', view_profile, name="view_profile"),
    path('profile/update', update_profile, name="update_profile_api"),
    path('profile/update/password', update_password_get, name="update_password_get"),
    path('profile/api/update/password', update_password_api, name="update_password_api"),
    path('profile/edit', edit_profile, name="edit_profile"),
    path('api/signup', api_signup, name="user_signup_post"),
    path('profile/avatar/set', set_avatar, name="set_avatar"),
]
   