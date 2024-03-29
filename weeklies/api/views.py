import re
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
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
from classroom.ranking_utils import get_students_weekly_performance_chart_data
from weeklies.models import *
from .serializer import WeeklySerializer
from .permission import IsUserPartOfClassroom


@api_view(['POST'])
@permission_classes([IsAuthenticated and IsUserTeacher])
def createWeekly(request, cls_pk):
    try:
        classroom = Classroom.objects.get(pk=cls_pk)
    except Classroom.DoesNotExist:
        return Response({'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = WeeklySerializer(data=request.data)   
    classroom_weeklies = classroom.weekly_set.all().order_by('-weeknum')
    latest_weeknum = 0
    if len(classroom_weeklies) > 0:
        latest_wk = classroom_weeklies[0]
        latest_weeknum = latest_wk.weeknum
    serializer.initial_data['classroom'] = classroom.id
    serializer.initial_data['weeknum'] = latest_weeknum + 1
    if serializer.is_valid():
        weekly = serializer.save()
        weekly_url = reverse('weeklies:weeklydetail', kwargs={'cls_pk':classroom.id, 'weeknum':weekly.weeknum})
        return Response({'num_weeklies':latest_weeknum+1, 'weekly_url':weekly_url})
    else:
        return Response(serializer.errors)


class UpdateWeeklyAV(UpdateAPIView):
    serializer_class = WeeklySerializer
    permission_classes = [IsAuthenticated, IsUserTeacher]

    def get_queryset(self):
        return Weekly.objects.filter(pk=self.kwargs.get('pk'))

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_weekly(request, cls_pk, pk):
    weekly = get_object_or_404(Weekly, classroom_id=cls_pk, pk=pk)
    if request.user in weekly.classroom.teachers.all():
        new_topic = request.data.get('topic')
        if new_topic:
            try:
                weekly.topic = new_topic
                weekly.save()
            except Exception as e:
                return Response(data={'info':"cannot set the new topic"}, status=status.HTTP_400_BAD_REQUEST)
            pre_cls_files_pk = request.data.get("pre_class_files")
            if pre_cls_files_pk:
                for i in pre_cls_files_pk:
                    try:
                        file = PreClassFile.objects.get(weekly=weekly, pk=i)
                        file.delete()
                    except Exception as e:
                        return Response(data={"info":"some files cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            in_cls_files_pk = request.data.get("in_class_files")
            if in_cls_files_pk:
                for i in in_cls_files_pk:
                    try:
                        file = InClassFile.objects.get(weekly=weekly, pk=i)
                        file.delete()
                    except Exception as e:
                        return Response(data={"info":"some files cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            post_cls_files_pk = request.data.get("post_class_files")
            if post_cls_files_pk:
                for i in post_cls_files_pk:
                    try:
                        file = PostClassFile.objects.get(weekly=weekly, pk=i)
                        file.delete()
                    except Exception as e:
                        return Response(data={"info":"some files cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            pre_cls_tutos_pk = request.data.get("pre_class_tuto")
            if pre_cls_tutos_pk:
                for i in pre_cls_tutos_pk:
                    try:
                        tuto = PreClassTutorial.objects.get(weekly=weekly, pk=i)
                        tuto.delete()
                    except Exception as e:
                        return Response(data={"info":"some tutorials cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            in_cls_tutos_pk = request.data.get("in_class_tuto")
            if in_cls_tutos_pk:
                for i in in_cls_tutos_pk:
                    try:
                        tuto = InClassTutorial.objects.get(weekly=weekly, pk=i)
                        tuto.delete()
                    except Exception as e:
                        return Response(data={"info":"some tutorials cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            post_cls_tutos_pk = request.data.get("post_class_tuto")
            if post_cls_tutos_pk:
                for i in post_cls_tutos_pk:
                    try:
                        tuto = PostClassTutorial.objects.get(weekly=weekly, pk=i)
                        tuto.delete()
                    except Exception as e:
                        return Response(data={"info":"some tutorials cannot be deleted"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data={"info":"completed"}, status=status.HTTP_200_OK)
    else:
        return Response(data={'info':'Forbidded'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['DELETE'])
def delete_weekly(request, cls_pk, pk):
    weekly = get_object_or_404(Weekly, pk=pk, classroom__id=cls_pk)
    if request.user in weekly.classroom.teachers.all():
        classroom_url = reverse('classroom:classroom_detail', kwargs={'pk':weekly.classroom.id})
        weekly.delete()
        return Response({'info':'deleted', 'classroom_url':classroom_url}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)



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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request, cls_pk, pk):
    try:
        weekly = Weekly.objects.get(pk=pk, classroom__id=cls_pk)
    except Weekly.DoesNotExist:
        return Response({'status':'weekly not found'}, status=status.HTTP_404_NOT_FOUND)
    if not (request.user in weekly.classroom.teachers.all() or request.user in weekly.classroom.students.all()):
        return Response({'status':'user not permitted'}, status=status.HTTP_403_FORBIDDEN)
    post = Forumpost(
        weekly = weekly,
        author = request.user,
        postcontent = request.data.get('post_text', '')
    )
    post.save()
    edit_url = reverse("weeklies:edit_post", kwargs={"weekly_pk":post.weekly.id, "pk":post.id})
    response = {
        "id": post.id,
        "author_name": post.author.account.user_full_name,
        "inst_id": post.author.account.institutional_id,
        "is_teacher": post.author in post.weekly.classroom.teachers.all(),
        "avatar_url": post.author.account.avatar_url,
        "postcontent": post.postcontent,
        "post_time": post.added,
        "edit_url": edit_url
    }

    return Response(response, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def weekly_performance_api(request, cls_pk, pk):
    try:
        weekly = get_object_or_404(Weekly, classroom__id=cls_pk, pk=pk)
    except Exception as e:
        return Response(data={'info':'weekly not found'}, status=status.HTTP_404_NOT_FOUND)
    if not ((request.user in weekly.classroom.teachers.all()) or (request.user in weekly.classroom.students.all())):
        return Response(data={'info':'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    cache_name = f"{weekly.id}-performancedata"
    stats_data = cache.get(cache_name)
    if stats_data is None:
        stats_data = get_students_weekly_performance_chart_data(weekly=weekly)
        cache.set(cache_name, stats_data, timeout=3600)
    return Response(data=stats_data, status=status.HTTP_200_OK)