from dateutil import parser
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Classroom, ClassroomPost, PostAttachment, Comment, Assignment, AssignmentAttachment



def render_underDev(request):
    return render(request,"classroom/under_dev.html")


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
        if self.request.user in classroom.teachers.all():
            query_set = classroom.ongoing_tests
            if query_set.count() > 0:
                context['teacher_tests'] = query_set
        elif self.request.user in classroom.students.all():
            query_set = classroom.ongoing_tests.exclude(answersheet__user=self.request.user)
            if query_set.count() > 0:
                context['student_tests'] = query_set
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    template_name = 'classroom/post_detail.html'
    model = ClassroomPost
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom_post = self.get_object()
        threads = Comment.objects.filter(post=classroom_post, parent=None)
        context['threads'] = threads
        return context


@login_required
def edit_post(request, pk):
    return render_underDev(request)

@login_required
def delete_post(request, pk):
    return render_underDev(request)

@login_required
def view_assignment(request, pk):
    return render_underDev(request)

def tests_all(request, pk):
    return render_underDev(request)


@login_required
def create_assignment(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == "GET":
        return render(request, 'classroom/create_assignment.html', context={"classroom":classroom})
    elif request.method == "POST":
        assignment = Assignment(
            classroom = classroom,
            title = request.POST.get("title", " "),
            instructions = request.POST.get("post-descr", None),
            submission_deadline = parser.parse(request.POST.get("deadline"))
        )
        assignment.save()
        files = dict(request.FILES).get("attachement", False)
        if files:
            for file in files:
                AssignmentAttachment.objects.create(assignment=assignment, attached_file=file)
        return HttpResponse("ok")

@login_required
def join_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in classroom.teachers.all():
        return redirect('classroom:classroom_detail', pk=classroom.id)
    if request.user not in classroom.students.all():
        classroom.students.add(request.user)
        return HttpResponse(f'You\'ve joined to: {classroom.name}')
    return redirect('classroom:classroom_detail', pk=classroom.id)


@login_required
@csrf_exempt
def create_post(request, pk):
    if request.method == 'POST':
        classroom = get_object_or_404(Classroom, pk=pk)
        if request.user not in classroom.teachers.all():
            raise PermissionDenied()
        classroom_post = ClassroomPost(
            classroom = classroom,
            description = request.POST.get('post_description'),
            author = request.user
        )
        classroom_post.save()
        has_files = bool(request.FILES.get('files', False))
        if has_files:
            files_dict = dict(request.FILES)['files']
            if len(files_dict) > 0:
                for file in files_dict:
                    PostAttachment.objects.create(
                        classroom_post = classroom_post,
                        attached_file = file
                    )
        return JsonResponse({'status':'completed'})
