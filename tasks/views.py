from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from classroom.models import Classroom

def create_task(request, cls_pk):
    if request.method == "GET":
        classroom = get_object_or_404(Classroom, pk=cls_pk)
        return render(request, 'tasks/create_task.html', context={'classroom':classroom})
    elif request.method == "POST":
        return HttpResponse(str(dict(request.POST)))
