from excel_response import ExcelResponse
from dateutil import parser
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .utilities import get_float_or_none, prepare_excel_file_data
from .models import (Classroom, ClassroomPost, PostTopic, PostAttachment,
                     Comment, Assignment, AssignmentAttachment, AssessmentMeta, Assessment)



def render_underDev(request):
    return render(request,"classroom/under_dev.html")

def render_info_or_error(request, heading, description, css_class="info"):
    context = {}
    context['heading'] = heading
    context['description'] = description
    context['css_class'] = css_class
    return render(request, 'classroom/infoerror.html', context=context)


def starter_homepage(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'account'):
            return redirect('classroom:homepage')
        else:
            return render_info_or_error(request, "No Classroom Account", "This is an admin account. Please create a general account to access this section")
    else:
        return render(request, "classroom/homepage.html")


class ClassesDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'classroom/classes_home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        my_teachings = Classroom.objects.filter(teachers=self.request.user).order_by('created')
        my_learnings = Classroom.objects.filter(students=self.request.user, active=True).order_by('created')
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
    
    def get_object(self):
        classroom = super().get_object()
        if self.request.user in classroom.teachers.all():
            return classroom
        else:
            if (self.request.user not in classroom.students.all()) or (not classroom.active):
                raise Http404
            else:
                return classroom
                
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = self.get_object()
        join_link = self.request.build_absolute_uri(reverse("classroom:join_classroom", args=(classroom.join_code,)))
        invitation_text = f"""Join {classroom.name} by using this code: {classroom.join_code}\nor by using this url: {join_link}"""
        context["invitation_text"] = invitation_text
        if self.request.user in classroom.teachers.all():
            query_set = classroom.ongoing_tests
            if query_set.count() > 0:
                context['teacher_tests'] = query_set
        elif self.request.user in classroom.students.all():
            query_set = classroom.students_non_participating_ongoing_tests(student=self.request.user)
            unsubmitted_tests = self.request.user.account.classroom_unsubmitted_tests(classroom)
            if (query_set.count() + unsubmitted_tests.count()) > 0:
                context['has_student_tests'] = True
                if query_set.count() > 0:
                    context['student_tests'] = query_set
                if unsubmitted_tests.count() > 0:
                    context['unsubmitted_tests'] = unsubmitted_tests
        return context


class ClassroomConnections(LoginRequiredMixin, DetailView):
    template_name = 'classroom/view_peoples.html'
    model = Classroom
    def get_object(self):
        classroom = super().get_object()
        if (self.request.user in classroom.teachers.all()) or (self.request.user in classroom.students.all()):
            return classroom
        else:
            raise Http404
        

class ClassroomAbout(LoginRequiredMixin, DetailView):
    template_name = 'classroom/classroom_about.html'
    model = Classroom
    def get_object(self):
        classroom = super().get_object()
        if (self.request.user in classroom.teachers.all()) or (self.request.user in classroom.students.all()):
            return classroom
        else:
            raise Http404
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom = context['classroom']
        context["join_link"] = self.request.build_absolute_uri(reverse("classroom:join_classroom", args=(classroom.join_code,)))
        return context
        
        
        

class PostDetail(LoginRequiredMixin, DetailView):
    template_name = 'classroom/post_detail.html'
    model = ClassroomPost
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classroom_post = self.get_object()
        threads = Comment.objects.filter(post=classroom_post, parent=None).order_by('comment_time')
        context['threads'] = threads
        return context


@login_required
def create_assessment(request, pk):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom, pk=pk)
        if request.user in classroom.teachers.all():
            assessmentmeta_data = {}
            assessmentmeta_data['classroom'] = classroom
            assessmentmeta_data['attendance_marks'] = get_float_or_none(request.POST.get("attendance"))
            assessmentmeta_data['classtest_marks'] = get_float_or_none(request.POST.get("classtest"))
            assessmentmeta_data['pre_class_marks'] = get_float_or_none(request.POST.get("pre-cls-marks"))
            assessmentmeta_data['in_class_marks'] = get_float_or_none(request.POST.get("in-cls-marks"))
            assessmentmeta_data['post_class_marks'] = get_float_or_none(request.POST.get("post-cls-marks"))
            if all([data!=None for data in assessmentmeta_data.values()]):
                meta = AssessmentMeta.objects.create(**assessmentmeta_data)
                for student in classroom.students.all():
                    Assessment.objects.create(meta=meta, student=student)
                return redirect('classroom:view_assessment', pk=classroom.id)
            else:
                return render_info_or_error(request, "ERROR 400", "Bad Request", 'error')
        else:
            return render_info_or_error(request, "ERROR 403", "Access Denied", 'error')


@login_required
def view_assessment(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    context = {}
    context['classroom'] = classroom
    
    if request.user in classroom.teachers.all():
        if hasattr(classroom, "assessmentmeta"):
            context['meta'] = classroom.assessmentmeta
        return render(request, 'classroom/assessment_list.html', context=context)
    elif request.user in classroom.students.all():
        assessment_qs = Assessment.objects.filter(student=request.user, meta__classroom=classroom)
        if len(assessment_qs) > 0:
            context['assessment'] = assessment_qs[0]
        return render(request, 'classroom/assessment_student.html', context=context)
    else:
        return render_info_or_error(request, "ERROR 403", "Access Denied", 'error')


@login_required
def view_student_assessment(request, cls_pk, pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    context = {}
    context['classroom'] = classroom
    if request.user in classroom.teachers.all():
        assessment = get_object_or_404(Assessment, pk=pk, meta__classroom=classroom)
        context['assessment'] = assessment
        return render(request, 'classroom/assessment_student.html', context=context)
    

@login_required
def download_assessment_excel(request, cls_pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    if request.user in classroom.teachers.all():
        if hasattr(classroom, 'assessmentmeta'):
            meta = classroom.assessmentmeta
            data = prepare_excel_file_data(meta)
            return ExcelResponse(data=data, output_filename=f"{classroom.name} Assessment Report")
        else:
            return render_info_or_error(request, 'No Metadata', 'No assessment meta found! Please define first.')
    else:
        return render_info_or_error(request, "ERROR 403", "Access Denied", 'error')
        

@login_required
def view_assessment_printf(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    meta_qs = AssessmentMeta.objects.filter(classroom=classroom)
    if len(meta_qs) == 0:
        return render_info_or_error(request, 'No Metadata', 'No assessment meta found! Please define first.')
    return render(request, 'classroom/assessment_print.html', context={'meta':meta_qs[0]})


@login_required
def edit_post(request, pk):
    classroom_post = get_object_or_404(ClassroomPost, pk=pk)
    return render(request, 'classroom/post_edit.html', context={'post':classroom_post})

@login_required
def delete_post(request, pk):
    classroom_post = get_object_or_404(ClassroomPost, pk=pk)
    return render(request, 'classroom/post_delete.html', context={'post':classroom_post})

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
def create_classroom(request):
    if request.method == "GET":
        if request.user.account.is_student:
            return render_info_or_error(request, 'Bad Request', "You cannot create any classroom")
        return render(request, "classroom/create_classroom.html")

@login_required
def edit_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in classroom.teachers.all():
        return render(request, "classroom/edit_classroom.html", context={"classroom":classroom})
    else:
        return render_info_or_error(request, "Unauthorized", "You have no permission to perform this action", "error")

@login_required
def join_classroom(request, cls_code):
    try:
        classroom = Classroom.objects.get(join_code=cls_code)
    except Classroom.DoesNotExist:
        return render_info_or_error(request, "Invalid Link", "This not a valid invitatin link of any existing classroom", "error")
    if request.user in classroom.teachers.all():
        return redirect('classroom:classroom_detail', pk=classroom.id)
    elif request.user not in classroom.students.all():
        classroom.students.add(request.user)
        return render_info_or_error(request, "Joined Successfully", f'You\'ve joined to: {classroom.name}', 'info')
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
        # adding topics
        topics_str = request.POST.get('topics', '')
        if len(topics_str) > 0:
            topics = topics_str.split(',')
            for topic in topics:
                topicStrId = topic.replace(' ', '').lower()
                topics_querySet = PostTopic.objects.filter(str_id=topicStrId, classroom=classroom)
                if len(topics_querySet) == 0:
                    post_topic = PostTopic.objects.create(name=topic, str_id=topicStrId, classroom=classroom)
                else:
                    post_topic = topics_querySet[0]
                classroom_post.topics.add(post_topic)
        return JsonResponse({'status':'completed'})


@login_required
@csrf_exempt
def uploadPostFile(request, pk):
    classroom_post = get_object_or_404(ClassroomPost, pk=pk)
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
    
# under dev.

@login_required
def topic_posts(request, pk, topic_id):
    topic = get_object_or_404(PostTopic, classroom=pk, str_id=topic_id)
    return render(request, 'classroom/topicdetail.html', context={'topic':topic})


@login_required
def classroom_assignment(request, pk):
    return render_underDev(request)

@login_required
def classroom_students(request, pk):
    return render_underDev(request)

@login_required
def classroom_groups(request, pk):
    return render_underDev(request)

@login_required
def classroom_files(request, pk):
    return render_underDev(request)