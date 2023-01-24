from dateutil import parser
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from classroom.models import Classroom
from weeklies.models import Weekly
from tasks.models import Task, TaskAttachment, Group, Work, WorkAttachment
from tasks.utils import random_subsets

def create_task(request, cls_pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    if request.method == "GET":
        return render(request, 'tasks/create_task.html', context={'classroom':classroom})
    elif request.method == "POST":
        task_obj_kwargs = {"classroom":classroom}
        weekly_pk = request.GET.get('weekly', None)
        if weekly_pk != None:
            weekly = get_object_or_404(Weekly, pk=weekly_pk)
            task_obj_kwargs['weekly'] = weekly
        else:
            task_obj_kwargs['weekly'] = None
        task_obj_kwargs['title'] = request.POST.get('title', None)
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
        print('creating groups')
        students_user_list = list(classroom.students.all())
        print(students_user_list)
        print(num_group_members)
        group_userlists = random_subsets(students_user_list, num_group_members)
        print(group_userlists)
        for user_list in group_userlists:
            print(user_list)
            group = Group.objects.create(task=task)
            group.members.add(*user_list)
        
        return HttpResponse('Task Created')


class TaskDetail(LoginRequiredMixin, DetailView):
    template_name = 'tasks/view_task.html'
    model = Task
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

