from django.shortcuts import render

# Create your views here.
def weeklyDetail(request, cls_pk, weeknum):
    return render(request, 'weeklies/weekly_teacher.html')