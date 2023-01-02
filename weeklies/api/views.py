import re
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from classroom.api.permission import IsUserTeacher
from classroom.models import Classroom

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createWeekly(request, pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response({'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    print(dict(request.data))