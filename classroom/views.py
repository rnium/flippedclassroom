import django
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Classroom


class ClassesDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'classroom/classes_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        my_teachings = Classroom.objects.filter(teachers=self.request.user)
        my_learnings = Classroom.objects.filter(students=self.request.user)
        classrooms = {}
        if len(my_teachings) > 0:
            classrooms['my_teachings'] = my_teachings
        if len(my_learnings) > 0:
            classrooms['my_learnings'] = my_learnings
        if len(classrooms) > 0:
            context['classrooms'] = classrooms
        return context


class ClassroomDetail(LoginRequiredMixin, DetailView):
    template_name = 'classroom/classroom_detail.html'
    model = Classroom
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_object()
        context["join_link"] = self.request.build_absolute_uri(reverse("classroom:join_classroom", args=(classroom.id,)))
        return context
    

def join_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in classroom.teachers.all():
        return redirect('classroom:classroom_detail', pk=classroom.id)
    if request.user not in classroom.students.all():
        classroom.students.add(request.user)
        return HttpResponse(f'You\'ve joined to: {classroom.name}')
    return redirect('classroom:classroom_detail', pk=classroom.id)
