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

class TestsHome(LoginRequiredMixin, TemplateView):
    template_name = 'exam/home.html'

    def get_context_data(self):
        data = super().get_context_data()
        data['tests'] = Test.objects.all()
        return data

class QuestionCreate(LoginRequiredMixin, DetailView):
    template_name = "exam/create_q.html"
    model = Classroom

@login_required
def take_test(request, pk):
    test = get_object_or_404(Test, pk=pk)
    try:
        answer_sheet = AnswerSheet.objects.get(test=test, user=request.user)
        if not answer_sheet.submit_time is None:
            return HttpResponse('you have already submitted your answer sheet')
    except AnswerSheet.DoesNotExist:
        answer_sheet = AnswerSheet.objects.create(test=test, user=request.user)

    return render(request, 'exam/answer_q.html', context={'test':test, 'answer_sheet':answer_sheet})


@login_required
def answer_submit(request, pk):
    if request.method == "POST":
        answer_sheet = get_object_or_404(AnswerSheet, pk=pk)
        req_data = {**dict(request.POST), **dict(request.FILES)}
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
                if len(a_data) == 3:
                    data_kwargs['answer_img'] = request.FILES.get(i)
                else:
                    answer_text = req_data[i][0]
                    if len(answer_text) > 0:
                        data_kwargs['answer_text'] = answer_text
                    else:
                        continue
            
                DescriptiveAnswer.objects.create(**data_kwargs)

        answer_sheet.submit_time = timezone.now()
        answer_sheet.save()
        return redirect('homepage')
    else:
        return HttpResponse("method not allowed") 


