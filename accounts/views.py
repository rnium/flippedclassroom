from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

class LoginView(TemplateView):
    template_name = 'accounts/login.html'

class SignupView(TemplateView):
    template_name = 'accounts/signup.html'

@api_view(['POST'])
def api_login(request):
    # performs login through an api
    print(request.data)
    return Response({'status':'connected but invalid info'})
