from dateutil import parser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from weekly_test.models import WeeklyTest, AnswerSheet, DescriptiveAnswer
from .serializer import TestSerializer, QuestionSerializer, OptionSerializer, AnswerSheetSerializer
from .paginations import AnswerSheetPagination
from rest_framework.permissions import IsAuthenticated
from .permission import IsUserTeacherOfClassroom
from rest_framework.generics import ListAPIView
from weeklies.models import Weekly
from classroom.models import Classroom

@api_view(["POST"])
def create_test(request, pk):
    if request.method == "POST":
        weekly = get_object_or_404(Weekly, pk=pk)
        testserializer = TestSerializer(data=request.data.get('test'))
        cc = request.GET.get("contentcode", False)
        if cc != False:
            if cc == '0':
                testserializer.initial_data['preclass'] = True
            elif cc == '1':
                testserializer.initial_data['inclass'] = True
            elif cc == '2':
                testserializer.initial_data['postclass'] = True
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':'invalid contentcode'})
        schedule = parser.parse(testserializer.initial_data['schedule'])
        expiration = parser.parse(testserializer.initial_data['expiration'])
        testserializer.initial_data['weekly'] = weekly.id
        testserializer.initial_data['schedule'] = schedule
        testserializer.initial_data['expiration'] = expiration
        
        user = request.user
        if testserializer.is_valid():
            test = testserializer.save(user=user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=testserializer.errors)
        for question in request.data.get('questions'):
            question_data = question['meta']
            question_data['test'] = test.id
            questionserializer = QuestionSerializer(data=question_data)
            if questionserializer.is_valid():
                question_obj = questionserializer.save()
            else:
               return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':questionserializer.errors})
            if not question_data['is_descriptive']:
                for option in question['options']:
                    del option['id']
                    option['question'] = question_obj.id
                    option_serializer = OptionSerializer(data=option)
                    if option_serializer.is_valid():
                        option_serializer.save()
                    else:
                       return Response(status=status.HTTP_400_BAD_REQUEST, data={'error':option_serializer.errors})
        return Response(data=testserializer.data,status=status.HTTP_201_CREATED)


@api_view(['POST'])
def issue_answer_sheet(request):
    if request.method == "POST":
        answer_sheet_pk = request.data.get("answer_sheet_pk")
        try:
            ans_sheet = AnswerSheet.objects.get(pk=answer_sheet_pk)
        except AnswerSheet.DoesNotExist:
            return Response(data={'info': 'answersheet not found'}, status=status.HTTP_404_NOT_FOUND)
        duration_seconds = ans_sheet.test.duration_seconds
        starttime = ans_sheet.issue_time
        if starttime is None:
            starttime = timezone.now()
            ans_sheet.issue_time = starttime
            ans_sheet.save()
        endtime = starttime + timedelta(seconds=duration_seconds)
        return Response(data={'pk': answer_sheet_pk, 'duration':duration_seconds, 'endtime':endtime})


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_test(request, pk):
    test = get_object_or_404(WeeklyTest, pk=pk)
    if request.user in test.weekly.classroom.teachers.all():
        test.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def live_test_stats(request, cls_pk):
    try:
        classroom = Classroom.objects.get(pk=cls_pk)
    except Classroom.DoesNotExist:
        return Response(data={'info':'classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.user not in classroom.teachers.all():
        return Response(data={'info':'access denied'}, status=status.HTTP_403_FORBIDDEN)
    live_tests = []
    try:
        test_pks = request.data['test_pks']
    except Exception as e:
        return Response(data={'info':'bad request'}, status=status.HTTP_400_BAD_REQUEST)
    for test_pk in test_pks:
        try:
            test = WeeklyTest.objects.get(pk=test_pk)
            live_tests.append(test)
        except WeeklyTest.DoesNotExist:
            return Response(data={'info':'test not found'}, status=status.HTTP_404_NOT_FOUND)
    dataset = {}
    for l_test in live_tests:
        unit_data = {}
        unit_data['issued'] = l_test.num_answer_sheets
        unit_data['submitted'] = l_test.num_submitted_answer_sheets
        dataset[l_test.id] = unit_data
    live_test_data = {'lt_data':dataset}
    return Response(data=live_test_data, status=status.HTTP_200_OK)
    



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_score(request, answersheet_pk):
    answersheet = get_object_or_404(AnswerSheet, pk=answersheet_pk)
    if request.user not in answersheet.test.weekly.classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    for ans_dat in request.data:
        des_ans = get_object_or_404(DescriptiveAnswer, pk=ans_dat['pk'], answer_sheet=answersheet)
        des_ans.score = ans_dat['score']
        des_ans.save()
    return Response(data={'status':'score updated'},status=status.HTTP_202_ACCEPTED)



class TestAnswersheetsView(ListAPIView):
    serializer_class = AnswerSheetSerializer
    permission_classes = [IsAuthenticated & IsUserTeacherOfClassroom]
    pagination_class = AnswerSheetPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        test =  get_object_or_404(WeeklyTest, pk=pk) 
        self.check_object_permissions(self.request, test)
        return test
    def get_queryset(self):
        test = self.get_object()
        answer_sheets = AnswerSheet.objects.filter(test=test, submit_time__isnull=False).order_by('submit_time')
        answer_sheets_sorted = sorted(answer_sheets, key=lambda o: o.time_taken)
        return answer_sheets_sorted