from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Account
from .utils import compress_image, check_account_data, check_user_data
from email.message import EmailMessage
from email.utils import formataddr
import ssl
import smtplib
from classroom.views import render_info_or_error



def send_html_email(receiver, subject, body):
    sender = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    host = settings.EMAIL_HOST
    port = settings.EMAIL_PORT
    
    em = EmailMessage()
    em['From'] = formataddr(("FlippedClassroom", sender))
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body, subtype='html')
    
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
    

def send_verification_email(request, user):
    current_site = get_current_site(request)
    email_subject = "Verify Your Email"
    receiver = user.email
    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    verification_url = request.build_absolute_uri(reverse("accounts:verify_user", args=(uid, token)))
    email_body = render_to_string('accounts/verification_mail.html', context={
        "user": user,
        "verification_url": verification_url,
    })
    send_html_email(receiver, email_subject, email_body)
    


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("classroom:homepage")
        else:
            return render(request=request, template_name='accounts/login.html')


class SignupView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("classroom:homepage")
        else:
            return render(request=request, template_name='accounts/signup.html')

            
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return redirect("classroom:starter")
    
@login_required
def view_profile(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/user_profile.html', context={'account':account})

@login_required
def edit_profile(request):
    account = request.user.account
    return render(request, 'accounts/user_edit_profile.html', context={'account':account})

@login_required
def update_password_get(request):
    return render(request, 'accounts/user_update_password.html')

@api_view(['POST'])
def api_login(request):
    # performs login through an api
    user = authenticate(username=request.data['email'], password=request.data['password'])
    if user:
        login(request, user)
        return Response({'status':'logged in'}, status=status.HTTP_200_OK)
    else:
        return Response({'status':'login failed'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def api_signup(request):
    email = request.data['email']
    user_queryset = User.objects.filter(email=email)
    if len(user_queryset) > 0:
        return Response({'status':'email used'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User(
            username = request.data['email'],
            email = request.data['email'],
            first_name = request.data['first_name'],
            last_name = request.data['last_name']
        )
        user.set_password(request.data['password'])
        user.save()
        account_kwargs = {}
        account_kwargs['user'] = user
        is_student = request.data['is_student']
        account_kwargs['is_student'] = is_student
        if is_student:
            account_kwargs['institution'] = request.data['institution']
            account_kwargs['institutional_id'] = request.data['institutional_id'] 
        Account.objects.create(**account_kwargs)
    except Exception as e:
        return Response({'status':str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    login(request, user=user)
    return Response({'status':"complete"}, status=status.HTTP_201_CREATED)



@login_required
def verify_user(request, uidb64, token):
    try :
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None
    
    if user and default_token_generator.check_token(user, token):
        account = user.account
        account.is_email_verified = True
        account.save()
        return render_info_or_error(request, "Verified", "Your email is successfully verified. You can return to dashboard")
    else:
        return render_info_or_error(request, "Error", "Invalid verification link", "error")


    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    # firstly checking email is used or not
    user_qs = User.objects.filter(email=request.data['user_data']['email'])
    if len(user_qs) > 0:
        if user_qs[0] != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    user_data = request.data['user_data']
    account_data = request.data['account_data']
    
    user = request.user
    account = user.account
    previous_mail = user.email
    
    try:
        check_user_data(user_data)
        check_account_data(account_data, request)
        for attr, val in user_data.items():
            setattr(user, attr, val)
        user.save()
        for attr, val in account_data.items():
            setattr(account, attr, val)
        if previous_mail != user.email:
            account.is_email_verified = False
        account.save()
    except Exception as e:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status=status.HTTP_200_OK)

@csrf_exempt
def set_avatar(request):
    if request.method == "POST":
        if len(request.FILES) > 0:
            user = request.user
            account = Account.objects.get(user=user)
            try:
                image_file = request.FILES.get('dp')
                compressed_image = compress_image(image_file)
            except ValidationError as e:
                return JsonResponse(data={'info': e.message}, status=400)
            if account.profile_picture is not None:
                account.profile_picture.delete(save=True)
            try:
                account.profile_picture = compressed_image
                account.save()
            except Exception as e:
                return JsonResponse(data={'info': 'Cannot save image'}, status=400)

            return JsonResponse({'status':'profile picture set'})
        

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def send_verification_email_api(request):
    try:
        send_verification_email(request, request.user)
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)        

     
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_password_api(request):
    username = request.user.username
    try:
        current_pass = request.data['current_password']
        new_pass = request.data['new_password']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user_obj = authenticate(username=username, password=current_pass)
    if user_obj != None and user_obj==request.user:
        user_obj.set_password(new_pass)
        user_obj.save()
        logout(request)
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

def forgot_password_get(request):
    return render(request, 'accounts/forgot.html')


@api_view(["POST"])
def send_recovery_email_api(request):
    email_subject = "Password Recovery"
    try:
        email = request.data['email']
    except Exception as e:
        return Response(data={"error":"no email provided"}, status=status.HTTP_400_BAD_REQUEST)
    user_qs = User.objects.filter(email=email)
    if len(user_qs) == 0:
        return Response(data={'info':'no user found with this email'}, status=status.HTTP_404_NOT_FOUND)
    user = user_qs[0]
    if not hasattr(user, 'account'):
        return Response(data={"info":"user has no account"}, status=status.HTTP_409_CONFLICT)

    uid = urlsafe_base64_encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
    recovery_url = request.build_absolute_uri(reverse("accounts:reset_password_get", args=(uid, token)))
    email_body = render_to_string('accounts/recovery_mail.html', context={
        "user": user,
        "recovery_url": recovery_url
    })
    try:
        send_html_email(user.email, email_subject, email_body)
    except Exception as e:
        return Response(data={'info':'cannot send email'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data={"info":"email sent"}, status=status.HTTP_200_OK)


def reset_password_get(request,  uidb64, token):
    try :
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
    except Exception as e:
        user = None
    
    if user and default_token_generator.check_token(user, token):
        uid = uidb64
        emaildb64 = urlsafe_base64_encode(force_bytes(user.email))
        reset_password_api_url = reverse("accounts:reset_password_api", args=(uid, emaildb64))
        return render(request, 'accounts/setup_new_pass.html', context={'reset_password_api_url':reset_password_api_url})
    else:
        return render_info_or_error(request, "Error", "Invalid or expired recovery link", "error")
    

@api_view(["POST"])
def reset_password_api(request, uidb64, emailb64):
    try :
        user_id = force_str(urlsafe_base64_decode(uidb64))
        email = force_str(urlsafe_base64_decode(emailb64))
        user = User.objects.get(pk=user_id, email=email)
    except Exception as e:
        user = None
    
    try:
        new_pass = request.data['new_password']
    except KeyError:
        return Response(data={"info":"required data not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    if user != None:
        user.set_password(new_pass)
        user.save()
        logout(request)
        return Response(data={"info":"password reset successful"},status=status.HTTP_200_OK)
    else:
        return Response(data={"info":"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
    