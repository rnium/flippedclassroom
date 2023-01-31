from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, FileResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Weekly, PreClassFile, InClassFile, PostClassFile, Forumpost
from django.urls import reverse
from classroom.views import render_info_or_error

# Create your views here.
@login_required
def weeklyDetail(request, cls_pk, weeknum):
    weekly = get_object_or_404(Weekly, classroom__id=cls_pk, weeknum=weeknum)
    classroom = weekly.classroom
    if request.user in classroom.teachers.all():
        return render(request, 'weeklies/weekly_teacher.html', context={'weekly':weekly})
    elif request.user in classroom.students.all():
        context = {}
        context['weekly'] = weekly
        pre_class_ongoing_tests = weekly.preClassOngoingTest.exclude(answersheet__user=request.user)
        in_class_ongoing_tests = weekly.inClassOngoingTest.exclude(answersheet__user=request.user)
        post_class_ongoing_tests = weekly.postClassOngoingTest.exclude(answersheet__user=request.user)
        if pre_class_ongoing_tests.count() > 0:
            context['pre_class_ongoing_tests'] = pre_class_ongoing_tests
        if in_class_ongoing_tests.count() > 0:
            context['in_class_ongoing_tests'] = in_class_ongoing_tests
        if post_class_ongoing_tests.count() > 0:
            context['post_class_ongoing_tests'] = post_class_ongoing_tests
        return render(request, 'weeklies/weekly_student.html', context=context)
    else:
        return HttpResponse("Unauthorized Access Denied")


@login_required
def edit_weekly_view(request, pk):
    weekly = get_object_or_404(Weekly, pk=pk)
    if request.user in weekly.classroom.teachers.all():
        return render(request, 'weeklies/weekly_edit.html', context={'weekly':weekly})
    else:
        return render_info_or_error(request, "Unauthorized", "Action not permitted", 'error')
    

@login_required
def delete_weekly_view(request, pk):
    weekly = get_object_or_404(Weekly, pk=pk)
    if request.user in weekly.classroom.teachers.all():
        return render(request, 'weeklies/weekly_delete.html', context={'weekly':weekly})
    else:
        return render_info_or_error(request, "Unauthorized", "Action not permitted", 'error')

@login_required
@csrf_exempt
def addFiles(request, weekly_pk):
    if request.method == 'POST':
        weekly = get_object_or_404(Weekly, pk=weekly_pk)
        if request.user not in weekly.classroom.teachers.all():
            raise PermissionDenied()
        has_files = bool(request.FILES.get('files', False))
        if has_files:
            files_dict = dict(request.FILES)['files']
            if len(files_dict) > 0:
                must_study = request.POST.get('must_study', False)
                if request.POST.get('preclass', False):
                    for file in files_dict:
                        PreClassFile.objects.create(
                            weekly = weekly,
                            must_study = must_study,
                            attached_file = file
                        )
                elif request.POST.get('inclass', False):
                    for file in files_dict:
                        InClassFile.objects.create(
                            weekly = weekly,
                            must_study = must_study,
                            attached_file = file
                        )
                elif request.POST.get('postclass', False):
                    for file in files_dict:
                        PostClassFile.objects.create(
                            weekly = weekly,
                            must_study = must_study,
                            attached_file = file
                        )
        return JsonResponse({'status':'completed'})
    else:
        return JsonResponse({'error':'Method not allowed'})


@login_required
def downloadFile(request, weekly_pk, pk):
    if request.method == "GET":
        contentcode = request.GET.get('contentcode', False)
        response = None
        if contentcode != False:
            if contentcode == "0":
                file_obj = get_object_or_404(PreClassFile, pk=pk, weekly__id=weekly_pk)
                file_path = file_obj.attached_file.path
                response = FileResponse(open(file_path, 'rb'))
            elif contentcode == "1":
                file_obj = get_object_or_404(InClassFile, pk=pk, weekly__id=weekly_pk)
                file_path = file_obj.attached_file.path
                response = FileResponse(open(file_path, 'rb'))
            elif contentcode == "2":
                file_obj = get_object_or_404(PostClassFile, pk=pk, weekly__id=weekly_pk)
                file_path = file_obj.attached_file.path
                response = FileResponse(open(file_path, 'rb'))
            else:
                return HttpResponse('Invalid ContentCode')
            return response
        else:
            HttpResponse('Invalid Request')
                

@login_required
def edit_post(request, weekly_pk, pk):
    post = get_object_or_404(Forumpost, pk=pk, weekly__pk=weekly_pk, author=request.user)
    if request.method == "GET":
        return render(request, 'weeklies/edit_weekly_forum.html', context={'post':post})
    elif request.method == "POST":
        postcontent = request.POST.get("post_content", False)
        print(postcontent)
        if postcontent != False:
            if len(postcontent) < 1:
                return HttpResponse("Post content cannot be empty")
            else:
                post.postcontent = postcontent
                post.save()
                return redirect("weeklies:weeklydetail", cls_pk=post.weekly.classroom.id, weeknum=post.weekly.weeknum)
        else:
            return HttpResponse("Invalid form")
    