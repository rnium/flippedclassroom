from django.urls import path
from .views import (LoginView, SignupView, LogoutView, 
                    api_login, api_signup, set_avatar, view_profile, send_verification_email_api, 
                    edit_profile, update_profile, update_password_get, update_password_api, verify_user,
                    send_recovery_email_api, reset_password_get, forgot_password_get, reset_password_api)

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name="user_login_get"),
    path('api/login', api_login, name="user_login_post"),
    path('logout/', LogoutView.as_view(), name="user_logout"),
    path('signup/', SignupView.as_view(), name="user_signup_get"),
    path('api/verify/sendmail', send_verification_email_api, name="send_verification_email_api"),
    path('verify/<uidb64>/<token>', verify_user, name="verify_user"),
    path('recovery', forgot_password_get, name="forgot_password_get"),
    path('api/recovery/sendmail', send_recovery_email_api, name="send_recovery_email_api"),
    path('recovery/<uidb64>/<token>', reset_password_get, name="reset_password_get"),
    path('api/recovery/setpassword/<uidb64>/<emailb64>', reset_password_api, name="reset_password_api"),
    path('profile/<int:pk>', view_profile, name="view_profile"),
    path('profile/update', update_profile, name="update_profile_api"),
    path('profile/update/password', update_password_get, name="update_password_get"),
    path('profile/api/update/password', update_password_api, name="update_password_api"),
    path('profile/edit', edit_profile, name="edit_profile"),
    path('api/signup', api_signup, name="user_signup_post"),
    path('profile/avatar/set', set_avatar, name="set_avatar"),
]
   