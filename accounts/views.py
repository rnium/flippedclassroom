from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from .models import Account

class LoginView(TemplateView):
    template_name = 'accounts/login.html'

class SignupView(TemplateView):
    template_name = 'accounts/signup.html'


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
            institution = request.data['institution']
        )
    except Exception as e:
        print(e)
        return Response({'status':'email used'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    # login(user)
    return Response({'status':"complete"}, status=status.HTTP_201_CREATED)

