from dateutil import parser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from datetime import timedelta
from exam.models import Test, AnswerSheet
from .serializer import TestSerializer, QuestionSerializer, OptionSerializer, AnswerSheetSerializer
from .paginations import AnswerSheetPagination
from rest_framework.permissions import IsAuthenticated
from .permission import IsUserTeacherOfClassroom
from rest_framework.generics import ListAPIView
from classroom.models import Classroom

@api_view(["POST"])
def create_test(request, pk):
    if request.method == "POST":
        classroom = get_object_or_404(Classroom, pk=pk)
        testserializer = TestSerializer(data=request.data.get('test'))
        schedule = parser.parse(testserializer.initial_data['schedule'])
        testserializer.initial_data['classroom'] = classroom.id
        testserializer.initial_data['schedule'] = schedule
        user = request.user
        if testserializer.is_valid():
            test = testserializer.save(user=user)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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


@api_view(["POST"])
@permission_classes([IsAuthenticated & IsUserTeacherOfClassroom])
def change_test_expiration_status(request):
    try:
        test = Test.objects.get(pk=request.data.get('test_id'))
    except Test.DoesNotExist:
        return Response(data={'info': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)
    test.expired = request.data.get('is_expired', False)
    test.save()
    return Response(data={'info': 'success', 'expired':test.expired}, status=status.HTTP_200_OK)

class TestAnswersheetsView(ListAPIView):
    serializer_class = AnswerSheetSerializer
    permission_classes = [IsAuthenticated & IsUserTeacherOfClassroom]
    pagination_class = AnswerSheetPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        test =  get_object_or_404(Test, pk=pk) 
        self.check_object_permissions(self.request, test)
        return test
    def get_queryset(self):
        test = self.get_object()
        answer_sheets = AnswerSheet.objects.filter(test=test, submit_time__isnull=False).order_by('-submit_time')
        return answer_sheets