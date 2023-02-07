from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from weekly_test.models import WeeklyTest, AnswerSheet, Question, McqOption, McqAnswer, DescriptiveAnswer
from weeklies.models import Weekly
from classroom.views import render_underDev, render_info_or_error
from django.http import HttpResponse, Http404


def home(request):
    return render(request, 'weekly_test/home.html')

class QuestionCreate(LoginRequiredMixin, DetailView):
    template_name = "weekly_test/create_q.html"
    model = Weekly

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cc = self.request.GET.get('contentcode', 10)
        context['contentcode'] = cc
        if cc == "0":
            context['section'] = 'Pre Class'
        elif cc == "1":
            context['section'] = 'In Class'
        elif cc == "2":
            context['section'] = 'Post Class'
        
        return context


# class TestView(LoginRequiredMixin, DetailView):
#     template_name = "weekly_test/viewresults.html"
#     model = WeeklyTest
    
#     def get_object(self):
#         test = super().get_object()
#         if self.request.user not in test.weekly.classroom.teachers.all():
#             raise Http404
#         return test
    

@login_required
def view_test(request, pk):
    test = get_object_or_404(WeeklyTest, pk=pk)
    if request.user in test.weekly.classroom.teachers.all():
        return render(request, "weekly_test/viewresults.html", context={"weeklytest":test})
    elif request.user in test.weekly.classroom.students.all():
        if test.expiration >= timezone.now():
            return render_info_or_error(request, "TEST ONGOING", "Return to dashboard to perticipate", "info")
        answersheet_qs = AnswerSheet.objects.filter(test=test, user=request.user)
        if len(answersheet_qs) == 0:
            return render_info_or_error(request, "No Answersheet", "You Haven't participated", "info")
        answersheet = answersheet_qs[0]
        return redirect("weekly_test:view_answersheet", pk=answersheet.id) 


class AnswersheetView(LoginRequiredMixin, DetailView):
    template_name = "weekly_test/view_answersheet.html"
    model = AnswerSheet
    
    def get_object(self):
        sheet = super().get_object()
        if not (self.request.user in sheet.test.weekly.classroom.teachers.all() or self.request.user in sheet.test.weekly.classroom.students.all()):
            raise Http404
        return sheet


def view_answersheet(request, pk):
    sheet = get_object_or_404(AnswerSheet, pk=pk)
    if request.user in sheet.test.weekly.classroom.teachers.all():
        return render(request, "weekly_test/view_answersheet.html", context={"answersheet":sheet})
    elif request.user == sheet.user:
        timenow = timezone.now()
        if sheet.submit_time == None:
            endtime = sheet.issue_time + timedelta(seconds=sheet.test.duration_seconds)
            if endtime < timenow:
                return render_info_or_error(request, "Unsubmitted", "Your answersheet is not submitted", "error")
            else:
                return redirect("weekly_test:take_test", pk=sheet.test.id)
        else:
            if sheet.test.expiration > timenow:
               return render_info_or_error(request, "TEST ONGOING", "Answersheet will be available after test finishes", "info")
            else:
                return render(request, "weekly_test/view_answersheet.html", context={"answersheet":sheet})
    
    else:
        return render_info_or_error(request, "Unauthorized", "You cannot view this answersheet", "error")



@login_required
def delete_test_get(request, pk):
    test = get_object_or_404(WeeklyTest, pk=pk)
    return render(request, 'weekly_test/exam_delete.html', context={'weeklytest':test})

@login_required
def take_test(request, pk):
    test = get_object_or_404(WeeklyTest, pk=pk)
    user_answer_sheet_queryset = AnswerSheet.objects.filter(test=test, user=request.user)
    if user_answer_sheet_queryset.count() > 0:
        if user_answer_sheet_queryset[0].submit_time != None:
            return render(request, 'weekly_test/already_submitted.html', context={'answer_sheet':user_answer_sheet_queryset[0]})
            
    
    if request.method == "GET":
        if user_answer_sheet_queryset.count() > 0:
            if user_answer_sheet_queryset[0].issue_time != None:
                return render(request, 'weekly_test/answer_q.html', context={'test':test, 'answer_sheet':user_answer_sheet_queryset[0]})
        answer_sheet = AnswerSheet.objects.create(test=test, user=request.user)
        return render(request, 'weekly_test/answer_q.html', context={'test':test, 'answer_sheet':answer_sheet})

    elif request.method == "POST":
        answer_sheet = user_answer_sheet_queryset[0]
        req_data = dict(request.POST)
        del req_data['csrfmiddlewaretoken']
        for i in req_data:
            if i.startswith('mcq'):
                a_data = req_data[i][0].split('-')
                question = get_object_or_404(Question, pk=a_data[0])
                option = get_object_or_404(McqOption, pk=a_data[1])
                McqAnswer.objects.create(
                    answer_sheet = answer_sheet,
                    question = question,
                    option_chosen = option
                )
            elif i.startswith('des'):
                a_data = i.split('-')
                data_kwargs = {'answer_sheet':answer_sheet}
                data_kwargs['question'] = get_object_or_404(Question, pk=a_data[-1])
                answer_text = req_data[i][0]
                if len(answer_text) > 0:
                    data_kwargs['answer_text'] = answer_text
                else:
                    continue
                DescriptiveAnswer.objects.create(**data_kwargs)
        for file in request.FILES:
            file_data = file.split('-')
            data_kwargs = {'answer_sheet':answer_sheet}
            data_kwargs['question'] = get_object_or_404(Question, pk=file_data[-1])
            data_kwargs['answer_img'] = request.FILES.get(file)
            DescriptiveAnswer.objects.create(**data_kwargs)
        answer_sheet.submit_time = timezone.now()
        answer_sheet.save()
        return render(request, 'weekly_test/submit_answer.html', context={'answer_sheet':answer_sheet})


@login_required
def classroom_tests(request, pk):
    return render_underDev(request)