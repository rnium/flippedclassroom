import re
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from classroom.api.permission import IsUserTeacher
from classroom.models import Classroom
from .serializer import WeeklySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createWeekly(request, cls_pk):
    print(request.data)
    try:
        classroom = Classroom.objects.get(pk=cls_pk)
    except Classroom.DoesNotExist:
        return Response({'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = WeeklySerializer(data=request.data)   
    num_weeklies = classroom.weekly_set.filter(classroom=cls_pk).count()
    serializer.initial_data['classroom'] = classroom.id
    serializer.initial_data['weeknum'] = num_weeklies + 1
    if serializer.is_valid():
        weekly = serializer.save()
        return Response({'num_weeklies':num_weeklies, 'wid':weekly.id})
    else:
        return Response(serializer.errors)