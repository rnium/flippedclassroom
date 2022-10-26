from optparse import Option
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Test, AnswerSheet, Question, McqOption, McqAnswer, DescriptiveAnswer
from classroom.models import Classroom
from django.http import HttpResponse
# Create your views here.
def home(request):
    return render(request, 'exam/home.html')

class QuestionCreate(LoginRequiredMixin, DetailView):
    template_name = "exam/create_q.html"
    model = Classroom

class TestView(LoginRequiredMixin, DetailView):
    template_name = "exam/viewresults.html"
    model = Test

@login_required
def take_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    user_answer_sheet_queryset = AnswerSheet.objects.filter(test=test, user=request.user)
    if user_answer_sheet_queryset.count() > 0:
        if user_answer_sheet_queryset[0].submit_time != None:
            return render(request, 'exam/already_submitted.html', context={'answer_sheet':user_answer_sheet_queryset[0]})
    
    if request.method == "GET":
        answer_sheet = AnswerSheet.objects.create(test=test, user=request.user)
        return render(request, 'exam/answer_q.html', context={'test':test, 'answer_sheet':answer_sheet})

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
        return render(request, 'exam/submit_answer.html', context={'answer_sheet':answer_sheet})

