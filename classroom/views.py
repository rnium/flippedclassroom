from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Classroom


class ClassesDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'classroom/classes_home.html'
    def get_context_data(self, **kwargs):
        my_teachings = Classroom.objects.filter(teachers=self.request.user)
        my_learnings = Classroom.objects.filter(students=self.request.user)
        print(my_teachings)
        print(my_learnings)
        return super().get_context_data()
