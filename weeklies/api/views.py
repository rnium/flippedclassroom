import re
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from urllib.parse import urlparse, parse_qs
from weeklies.api.permission import IsUserTeacher
from classroom.models import Classroom
from weeklies.models import *
from .serializer import WeeklySerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated and IsUserTeacher])
def createWeekly(request, cls_pk):
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
        weekly_url = reverse('weeklies:weeklydetail', kwargs={'cls_pk':classroom.id, 'weeknum':weekly.weeknum})
        return Response({'num_weeklies':num_weeklies, 'weekly_url':weekly_url})
    else:
        return Response(serializer.errors)



class UpdateWeeklyAV(UpdateAPIView):
    serializer_class = WeeklySerializer
    permission_classes = [IsAuthenticated, IsUserTeacher]

    def get_queryset(self):
        return Weekly.objects.filter(pk=self.kwargs.get('pk'))


@api_view(['POST'])
@permission_classes([IsAuthenticated and IsUserTeacher])
def add_tutorial(request, cls_pk, pk):
    weekly = get_object_or_404(Weekly, pk=pk)
    video_url = request.data['yt_url']
    parse_result = urlparse(video_url)
    try:
        video_id = parse_qs(parse_result.query).get('v')[0]
    except TypeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    vid_descr = request.data['description']
    if request.data['pre_class']:
        PreClassTutorial.objects.create(weekly=weekly, yt_id=video_id, description=vid_descr)
    elif request.data['in_class']:
        InClassTutorial.objects.create(weekly=weekly, yt_id=video_id, description=vid_descr)
    elif request.data['post_class']:
        PostClassTutorial.objects.create(weekly=weekly, yt_id=video_id, description=vid_descr)
    data = {
        "video_id": video_id,
        "description": vid_descr
    }
    return Response(data)
