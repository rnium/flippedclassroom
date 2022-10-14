from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from exam.models import Test, AnswerSheet
from .serializers import TestSerializer, QuestionSerializer, OptionSerializer

@api_view(["GET", "POST"])
def create_test(request):
    if request.method == "GET":
        tests = Test.objects.all()
        serializer = TestSerializer(tests, many=True)
        print(request.user)
        return Response(serializer.data)
    elif request.method == "POST":
        testserializer = TestSerializer(data=request.data.get('test'))
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
               print(questionserializer.errors)
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
        return Response(data={"data":"created", "test_id":test.id},status=status.HTTP_201_CREATED)


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