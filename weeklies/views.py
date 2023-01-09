from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Weekly, PreClassFile, InClassFile, PostClassFile

# Create your views here.
def weeklyDetail(request, cls_pk, weeknum):
    weekly = get_object_or_404(Weekly, classroom__id=cls_pk, weeknum=weeknum)
    classroom = weekly.classroom
    if request.user in classroom.teachers.all():
        return render(request, 'weeklies/weekly_teacher.html', context={'weekly':weekly})
    else:
        return render(request, 'weeklies/weekly_student.html', context={'weekly':weekly})


@login_required
@csrf_exempt
def addFiles(request, weekly_pk):
    if request.method == 'POST':
        print(request.POST)
        # weekly = get_object_or_404(Weekly, pk=weekly_pk)
        # if request.user not in weekly.classroom.teachers.all():
        #     raise PermissionDenied()
        # has_files = bool(request.FILES.get('files', False))
        # if has_files:
        #     files_dict = dict(request.FILES)['files']
        #     if len(files_dict) > 0:
        #         must_study = request.POST.get('must_study', False)
        #         if request.POST.get('preclass', False):
        #             for file in files_dict:
        #                 PreClassFile.objects.create(
        #                     weekly = weekly,
        #                     must_study = must_study,
        #                     attached_file = file
        #                 )
        #         elif request.POST.get('inclass', False):
        #             for file in files_dict:
        #                 InClassFile.objects.create(
        #                     weekly = weekly,
        #                     must_study = must_study,
        #                     attached_file = file
        #                 )
        #         elif request.POST.get('postclass', False):
        #             for file in files_dict:
        #                 PostClassFile.objects.create(
        #                     weekly = weekly,
        #                     must_study = must_study,
        #                     attached_file = file
        #                 )
        return JsonResponse({'status':'completed'})