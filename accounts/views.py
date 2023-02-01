from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.decorators import login_required
from .models import Account

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
        return redirect("accounts:user_login_get")
    
@login_required
def view_profile(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/user_profile.html', context={'account':account})

@login_required
def edit_profile(request, pk):
    account = get_object_or_404(Account, pk=pk)
    return render(request, 'accounts/user_edit_profile.html', context={'account':account})


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
        Account.objects.create(
            user = user,
            institution = request.data['institution'],
            institutional_id = request.data['institutional_id']
        )
    except Exception as e:
        print(e)
        return Response({'status':'email used'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    login(request, user=user)
    return Response({'status':"complete"}, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    # firstly checking email is used or not
    user_qs = User.objects.filter(email=request.data['user_data']['email'])
    print(user_qs)
    if len(user_qs) > 0:
        if user_qs[0] != request.user:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    user_data = request.data['user_data']
    account_data = request.data['account_data']
    
    user = request.user
    account = user.account

    try:
        for attr, val in user_data.items():
            setattr(user, attr, val)
        user.save()
        for attr, val in account_data.items():
            setattr(account, attr, val)
        account.save()
    except Exception:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    return Response(status=status.HTTP_200_OK)

@csrf_exempt
def set_avatar(request):
    if request.method == "POST":
        if len(request.FILES) > 0:
            user = request.user
            account = Account.objects.get(user=user)
            account.profile_picture = request.FILES.get('dp')
            account.save()
            return JsonResponse({'status':'profile picture set'})