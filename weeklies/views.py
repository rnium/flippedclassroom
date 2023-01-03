from django.shortcuts import render, get_object_or_404
from .models import Weekly

# Create your views here.
def weeklyDetail(request, cls_pk, weeknum):
    weekly = get_object_or_404(Weekly, classroom__id=cls_pk, weeknum=weeknum)
    classroom = weekly.classroom
    if request.user in classroom.teachers.all():
        return render(request, 'weeklies/weekly_teacher.html', context={'weekly':weekly})
    else:
        return render(request, 'weeklies/weekly_student.html', context={'weekly':weekly})