from dateutil import parser
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import SuspiciousOperation
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from classroom.models import Classroom
from classroom.views import render_info_or_error
from weeklies.models import Weekly
from tasks.models import Task, TaskAttachment, Group, Work, WorkAttachment
from tasks.utils import random_subsets


# FBV
def create_task(request, cls_pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    if request.method == "GET":
        weekly_pk = request.GET.get('weekly', None)
        context = {}
        context['classroom'] = classroom
        if weekly_pk != None:
            weekly = get_object_or_404(Weekly, pk=weekly_pk)
            context['weeknum'] = weekly.weeknum
            contentcode = request.GET.get('contentcode', False)
            if contentcode != False:
                if contentcode == "0":
                    context['section'] = "PreClass"
                elif contentcode == "1":
                    context['section'] = "InClass"
                elif contentcode == "2":
                    context['section'] = "PostClass"
                else:
                    return HttpResponse("Invalid Contentcode")
        return render(request, 'tasks/create_task.html', context=context)
    elif request.method == "POST":
        task_obj_kwargs = {"classroom":classroom}
        weekly_pk = request.GET.get('weekly', None)
        if weekly_pk != None:
            weekly = get_object_or_404(Weekly, pk=weekly_pk)
            task_obj_kwargs['weekly'] = weekly
        else:
            task_obj_kwargs['weekly'] = None
        task_obj_kwargs['title'] = request.POST.get('title', None)
        marks = request.POST.get('marks', None)
        if marks != None:
            if len(marks) > 0:
                if marks.isdigit():
                    task_obj_kwargs['marks'] = int(marks)
        try:
            deadline = request.POST.get('deadline-datetime', None)
            task_obj_kwargs['deadline'] =  parser.parse(deadline)
        except:
            return HttpResponse("invalid date")
        instruction = request.POST.get('description', None)
        tasktype = request.POST.get('tasktype', None)
        if instruction != None:
            if len(instruction) > 0:
                task_obj_kwargs['instruction'] = instruction
        if tasktype != None:
            if tasktype == "group":
                global num_group_members
                num_group_members = request.POST.get('num-group-member', None)
                num_group_members = int(num_group_members)
                if num_group_members > classroom.students.count():
                    return HttpResponse("Invalid Group Member Count")
        contentcode = request.GET.get('contentcode', False)
        if contentcode != False:
            if contentcode == "0":
                task_obj_kwargs['preclass'] = True
            elif contentcode == "1":
                task_obj_kwargs['inclass'] = True
            elif contentcode == "2":
                task_obj_kwargs['postclass'] = True
        
        task = Task(**task_obj_kwargs)
        task.save()
        # attached files create
        has_files = bool(request.FILES.get('post-file', False))
        if has_files:
            files_dict = dict(request.FILES)['post-file']
            if len(files_dict) > 0:
                for file in files_dict:
                    TaskAttachment.objects.create(
                        task = task,
                        attached_file = file
                    )
        # creating groups
        if tasktype == 'group':
            students_user_list = list(classroom.students.all())
            group_userlists = random_subsets(students_user_list, num_group_members)
            for user_list in group_userlists:
                group = Group.objects.create(task=task)
                group.members.add(*user_list)
        
        return redirect('classroom:tasks:view_task', cls_pk=cls_pk, pk=task.id)

def view_task_file(request, cls_pk, pk):
    attachment = get_object_or_404(TaskAttachment, task__classroom__id=cls_pk, pk=pk)
    if not (request.user in attachment.task.classroom.teachers.all() or request.user in attachment.task.classroom.students.all()):
        raise Http404
    context = {}
    context['task_file'] = True
    context['current_file'] = attachment
    context['other_files'] = TaskAttachment.objects.filter(task=attachment.task).exclude(id=attachment.id)
    return render(request, "tasks/view_file.html", context=context)

def view_work_file(request, cls_pk, pk):
    attachment = get_object_or_404(WorkAttachment, work__task__classroom__id=cls_pk, pk=pk)
    if not (request.user in attachment.work.task.classroom.students.all()):
        raise Http404
    context = {}
    context['current_file'] = attachment
    context['other_files'] = WorkAttachment.objects.filter(work=attachment.work).exclude(id=attachment.id)
    return render(request, "tasks/view_file.html", context=context)


def delete_task_get(request, cls_pk, pk):
    task = get_object_or_404(Task, classroom__id=cls_pk, pk=pk)
    if request.user in task.classroom.teachers.all():
        return render(request, "tasks/delete_task.html", context={'task':task})
    else:
        return render_info_or_error(request, 'Unauthorized', 'You have no permission to perform this action', "error")
    

#CBV
class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = 'tasks/view_task.html'
    model = Task
    def get_object(self):
        task = super().get_object()
        if not (self.request.user in task.classroom.teachers.all() or self.request.user in task.classroom.students.all()):
            raise Http404
        return task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = context['task']
        group_type = task.is_group_task 
        if self.request.user in task.classroom.teachers.all():
            context['is_teacher'] = True
            if task.is_group_task:
                groups = Group.objects.filter(task=task)
                context['group_submissions'] = [g for g in groups if g.work_submitted]
                context['unsubmitting_groups'] = [g for g in groups if not g.work_submitted]
            else:
                context['indiv_submissions'] = Work.objects.filter(task=task, is_submitted=True, group=None)
                students = task.classroom.students.all()
                unsubmitting_indiv = []
                for s in students:
                    qs = Work.objects.filter(task=task, submission_by=s, is_submitted=True)
                    if len(qs) == 0:
                        unsubmitting_indiv.append(s)
                context['unsubmitting_indiv'] = unsubmitting_indiv
                
        elif self.request.user in task.classroom.students.all():
            if group_type:
                # fix this: A new student who just joined, have no group. If they click task detail show them that they were not assigned
                groups = Group.objects.filter(task=task, members=self.request.user)
                if len(groups)==0:
                    raise Http404
                group=groups[0]
                context['group'] = group
                if group.work:
                    context['work'] = group.work
            else:
                work_queryset = Work.objects.filter(task=task,submission_by=self.request.user)
                if len(work_queryset) > 0:
                    context['work'] = work_queryset[0]
                    
        return context


class WorkDetail(LoginRequiredMixin, DetailView):
    template_name = 'tasks/view_work.html'
    model = Work
    
    def get_object(self):
        work = super().get_object()
        if not self.request.user in work.task.classroom.teachers.all():
            raise Http404
        if not work.is_submitted:
            raise Http404
        return work


#API
@login_required
@csrf_exempt
def upload_work(request, cls_pk, pk):
    if request.method == 'POST':
        # not creating work if no files were added
        has_files = bool(request.FILES.get('files', False))
        files_dict = None
        if has_files:
            files_dict = dict(request.FILES)['files']
            if len(files_dict) < 1:
                raise SuspiciousOperation("No files included")
        else:
            raise SuspiciousOperation("Invalid Form")
        
        task = get_object_or_404(Task, classroom__id=cls_pk, pk=pk)
        new_work_obj_data = {"task":task}
        if task.is_group_task:
            group = get_object_or_404(Group, task=task, members=request.user)
            prev_work_of_grp = Work.objects.filter(task=task, group=group) # checking if group has any previous works
            if len(prev_work_of_grp) > 0:
                raise SuspiciousOperation('Group already has their work')
            new_work_obj_data['group'] = group
        else:
            prev_work_of_indiv = Work.objects.filter(task=task,submission_by=request.user) # checking if user has any previous works
            if len(prev_work_of_indiv) > 0:
                raise SuspiciousOperation("User already has their work")
        new_work_obj_data['submission_by'] = request.user
        work = Work.objects.create(**new_work_obj_data)
        
        # adding files
        for file in files_dict:
            WorkAttachment.objects.create(
                work = work,
                attached_file = file
            )
        return JsonResponse({'status':'completed'})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_work_submission_status(request, cls_pk, pk):
    try:
        work = Work.objects.get(pk=pk, task__classroom__id=cls_pk)
    except Work.DoesNotExist:
        return Response(data={'info': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)
    if work.task.is_group_task:
        if request.user not in work.group.members.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        if work.submission_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    if work.is_submitted:
        # if work has score, cannot be unsubmitted
        if work.score != None:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        work.is_submitted = False
    else:
        work.is_submitted = True
        work.submission_time = timezone.now()
    work.save()
    return Response(data={'info': 'success', 'is_submitted':work.is_submitted}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def delete_work(request, cls_pk, pk):
    try:
        work = Work.objects.get(pk=pk, task__classroom__id=cls_pk)
    except Work.DoesNotExist:
        return Response(data={'info': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)
    if work.task.is_group_task:
        if request.user not in work.group.members.all():
            return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        if work.submission_by != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
    
    # if work has score, cannot be deleted
    if work.score != None:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

    work.delete()
    return Response(data={'info': 'deleted', 'is_deleted':True}, status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_task(request, cls_pk, pk):
    task =  get_object_or_404(Task, classroom__id=cls_pk, pk=pk)
    if request.user in task.classroom.teachers.all():
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_work_score(request, cls_pk, pk):
    try:
        work = Work.objects.get(pk=pk, task__classroom__id=cls_pk, )
    except Work.DoesNotExist:
        return Response(data={'info': 'Work not found'}, status=status.HTTP_404_NOT_FOUND)
    if not work.is_submitted:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user not in work.task.classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    score = request.data['score']
    if (score > work.task.marks) or (score < 0):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    work.score = score
    work.save()
    return Response(data={'info': 'success', 'score':work.score}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_work_remarks(request, cls_pk, pk):
    try:
        work = Work.objects.get(pk=pk, task__classroom__id=cls_pk, )
    except Work.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if not work.is_submitted:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.user not in work.task.classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        remarks = request.data['remarks']
    except Exception as e:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    work.remarks = remarks
    work.save()
    return Response(status=status.HTTP_200_OK)