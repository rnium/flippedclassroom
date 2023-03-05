from datetime import timedelta
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from classroom.models import ClassroomPost, PostAttachment, Classroom, Comment, AssessmentMeta, Assessment, Congratulation
from classroom.ranking_utils import get_students_ranking_data, get_students_performance_chart_data
from .serializer import PostSerializer, ClassroomSerializer
from .permission import IsUserPartOfClassroom, IsUserTeacher
from .pagination import PostsPagination


class ClassroomPostsView(ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsUserPartOfClassroom]
    pagination_class = PostsPagination
    def get_object(self):
        pk = self.kwargs.get('pk')
        classroom =  get_object_or_404(Classroom, pk=pk) 
        self.check_object_permissions(self.request, classroom)
        return classroom
    def get_queryset(self):
        classroom = self.get_object()
        posts = ClassroomPost.objects.filter(classroom=classroom).order_by('-posted')
        return posts


class UpdateClassroomAV(UpdateAPIView):
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated, IsUserTeacher]

    def get_queryset(self):
        print(self.request.data)
        return Classroom.objects.filter(pk=self.kwargs.get('pk'))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def classroom_join_api(request):
    cls_code = request.GET.get('code', None)
    if cls_code == None:
        return Response(data={"info":"Code not provided"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        classroom = Classroom.objects.get(join_code=cls_code)
    except Classroom.DoesNotExist:
        return Response(data={"info":"Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
    if not request.user.account.is_student:
        return Response(data={"status":"Teacher cannot join classroom as a student"}, status=status.HTTP_400_BAD_REQUEST)
    if not classroom.active:
        return Response(data={"info":"Classroom is not active"}, status=status.HTTP_403_FORBIDDEN)
    if request.user in classroom.teachers.all():
        return Response(data={"info":"You're a teacher of this classroom"}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        if request.user in classroom.students.all():
            return Response(data={"info": f"You've already joined {classroom.name}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            classroom.students.add(request.user)
            classroom_dashboard = reverse("classroom:classroom_detail", args=(classroom.id,))
            return Response(data={"dashboard": classroom_dashboard}, status=status.HTTP_200_OK)
    


@csrf_exempt
@login_required
def set_banner(request, pk):
    if request.method == "POST":
        if len(request.FILES) > 0:
            classroom = Classroom.objects.get(pk=pk)
            if request.user not in classroom.teachers.all():
                return JsonResponse({'status':'Unauhtorized'})
            classroom.banner = request.FILES.get('dp')
            classroom.save()
            return JsonResponse({'status':'profile picture set'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_banner_to_default(request, pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.user not in classroom.teachers.all():
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if classroom.banner == None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    classroom.banner.delete(save=True)
    return Response(status=status.HTTP_200_OK)     


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def change_join_code(request, pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response(data={'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.user not in classroom.teachers.all():
        return Response(data={'status':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
    cls_code = get_random_string(6)
    classrooms_qs = Classroom.objects.filter(join_code=cls_code)
    while len(classrooms_qs) > 1:
        cls_code = get_random_string(6)
        classrooms_qs = Classroom.objects.filter(join_code=cls_code)
    classroom.join_code = cls_code
    classroom.save()
    return Response(data={'newcode':classroom.join_code}, status=status.HTTP_200_OK)     



@api_view(['POST'])
@permission_classes([IsAuthenticated & IsUserPartOfClassroom])
def post_comment(request, pk):
    try:
        post = ClassroomPost.objects.get(pk=pk)
    except ClassroomPost.DoesNotExist:
        return Response({'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    parent_comment = request.data.get('parent_comment_id')
    if parent_comment != None:
        try:
            parent = Comment.objects.get(pk=parent_comment)
        except Comment.DoesNotExist:
            return Response({'status':'comment not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        parent = None
    comment = Comment(
        post = post,
        author = request.user,
        parent = parent,
        comment_text = request.data.get('comment_text', '')
    )
    comment.save()
    response = {
        "parent_id": parent_comment,
        "id": comment.id,
        "author_name": comment.author.account.user_full_name,
        "avatar_url": comment.author.account.avatar_url,
        "cssClass": comment.cssClass,
        "comment_text": comment.comment_text,
        "comment_time": comment.comment_time,
        "num_comments": comment.post.num_comments,
    }

    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_classroom(request):
    if request.user.account.is_student:
        return Response(data={"status":"error"}, status=status.HTTP_400_BAD_REQUEST)
    serializer = ClassroomSerializer(data=request.data)
    cls_code = get_random_string(6)
    classrooms_qs = Classroom.objects.filter(join_code=cls_code)
    while len(classrooms_qs) > 1:
        cls_code = get_random_string(6)
        classrooms_qs = Classroom.objects.filter(join_code=cls_code)
    serializer.initial_data['join_code'] = cls_code
    if serializer.is_valid():
        classroom = serializer.save()
        classroom.teachers.add(request.user)
        response_data = {}
        response_data['name'] = classroom.name
        response_data['classroom_url'] = reverse("classroom:classroom_detail", args=(classroom.id,))
        response_data["join_link"] = request.build_absolute_uri(reverse("classroom:join_classroom", args=(classroom.join_code,)))
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"status":"error"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_classroom_api(request, pk):
    try:
        classroom = Classroom.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response(data={'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.user not in classroom.teachers.all():
        return Response(data={'status':'Unauthorized'},status=status.HTTP_401_UNAUTHORIZED)
    classroom.delete()
    homepage = reverse("classroom:homepage")
    return Response(data={"homepage":homepage}, status=status.HTTP_200_OK)
    
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_user_from_classroom(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    try:
        user_id = request.data['user_id']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(User, pk=user_id)
    if (user in classroom.teachers.all()) or (user in classroom.students.all()):
        if (request.user in classroom.teachers.all()):
            if request.user == user:
                if classroom.teachers.count() < 2:
                    return Response({'status':"user non-removable"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                  classroom.teachers.remove(user)  
            else:
                classroom.students.remove(user)
            return Response({'status':"user removed"}, status=status.HTTP_200_OK)
        elif (request.user in classroom.students.all()) and (request.user == user):
            classroom.students.remove(user)
            return Response({'status':"user removed"}, status=status.HTTP_200_OK)
        else:
            return Response({'info':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'info':'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated ])
def update_post_des_and_rm_files(request, pk):
    post = get_object_or_404(ClassroomPost, pk=pk)
    if request.user not in post.classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    new_descr = request.data.get("description", None)
    if new_descr:
        post.description = new_descr
        post.save()
    removed_files = request.data.get('removed_files', None)
    if removed_files != None:
        for file_pk in removed_files:
           try:
               posted_file = PostAttachment.objects.get(classroom_post=post, pk=file_pk)
           except PostAttachment.DoesNotExist:
               continue
           posted_file.delete()
    return Response(data={"info":"complete"}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_post(request, pk):
    post = get_object_or_404(ClassroomPost, pk=pk)
    if request.user not in post.classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    post.delete()
    return Response(data={"status":"deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_assessments(request, cls_pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    if request.user not in classroom.teachers.all():
        return Response(status=status.HTTP_403_FORBIDDEN)
    else:
        for a_data in request.data:
            assessment = get_object_or_404(Assessment, pk=a_data, meta__classroom=classroom)
            for attr, value in request.data[a_data].items():
                if attr == 'attendance_score':
                    if (value > assessment.meta.attendance_marks) or (value < 0):
                        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                    setattr(assessment, attr, value)
                elif attr == 'classtest_score':
                    if (value > assessment.meta.classtest_marks) or (value < 0):
                        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
                    setattr(assessment, attr, value)
            assessment.save()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_assessment_meta(request, cls_pk):
    classroom = get_object_or_404(Classroom, pk=cls_pk)
    if request.user in classroom.teachers.all():
        if hasattr(classroom, 'assessmentmeta'):
            classroom.assessmentmeta.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_teacher(request, pk):
    if request.user.account.is_student:
        return Response(data={"status":"student cannot be added as teacher"}, status=status.HTTP_400_BAD_REQUEST)
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.user in classroom.teachers.all():
        user_qs = User.objects.filter(email=request.data['email'])
        if len(user_qs) > 0:
            user = user_qs[0]
            if user in classroom.teachers.all():
                return Response(status=status.HTTP_208_ALREADY_REPORTED)
            elif user in classroom.students.all():
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                classroom.teachers.add(user)
                return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def congratulate_user(request, pk):
    try:  
        classroom = Classroom.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response(data={'info': "Classroom not found"}, status=status.HTTP_404_NOT_FOUND)
    try:  
        to_user = User.objects.get(pk=request.data['uid'])
    except Classroom.DoesNotExist:
        return Response(data={'info': "User not found"}, status=status.HTTP_404_NOT_FOUND)

    min_time_gap = timedelta(days=7)
    last_time = timezone.now() - min_time_gap
    congrats_qs = Congratulation.objects.filter(from_user=request.user, to_user=to_user, added__gt=last_time)
    if len(congrats_qs) > 0:
        return Response(data={'info': f"You've already congratulated {to_user.account.user_full_name} for his rank in this week"}, status=status.HTTP_400_BAD_REQUEST)
    if not ((request.user in classroom.teachers.all()) or (request.user in classroom.students.all()) or (to_user in classroom.students.all())):
        return Response(data={'info': "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
    congrats = Congratulation.objects.create(from_user=request.user, to_user=to_user)
    res_data = {'user_fullname':congrats.to_user.account.user_full_name}
    return Response(data=res_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ranking_api(request, cls_pk):
    try:
        classroom = get_object_or_404(Classroom, pk=cls_pk)
    except Exception as e:
        return Response(data={'info':'classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    if not ((request.user in classroom.teachers.all()) or (request.user in classroom.students.all())):
        return Response(data={'info':'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    rank_data = get_students_ranking_data(classroom, request.user)
    num_rankig = len(rank_data['ranked_students'])
    has_ranking = bool(num_rankig)
    data = {
        'num_rankig':num_rankig,
        'has_ranking':has_ranking,
        'data':rank_data
    }
    return Response(data=data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def classroom_performance_api(request, cls_pk):
    try:
        classroom = get_object_or_404(Classroom, pk=cls_pk)
    except Exception as e:
        return Response(data={'info':'classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    if not ((request.user in classroom.teachers.all()) or (request.user in classroom.students.all())):
        return Response(data={'info':'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    stats_data = get_students_performance_chart_data(classroom)
    
    num_stats = len(stats_data['studentData'])
    has_stats = bool(num_stats)
    
    data = {
        'has_stats':has_stats,
        'data':stats_data
    }
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_congrats_api(request, pk):
    try:
        classroom = get_object_or_404(Classroom, pk=pk)
    except Exception as e:
        return Response(data={'info':'classroom not found'}, status=status.HTTP_404_NOT_FOUND)
    if not ((request.user in classroom.teachers.all()) or (request.user in classroom.students.all())):
        return Response(data={'info':'forbidden'}, status=status.HTTP_403_FORBIDDEN)
    congrats = Congratulation.objects.filter(to_user=request.user, is_expired=False)
    res_list = []
    for i in congrats:
        unit_data = {}
        unit_data['sender_name'] = i.from_user.account.user_full_name
        unit_data['sender_avatar'] = i.from_user.account.avatar_url
        res_list.append(unit_data)
        i.is_expired = True
        i.save()
        
    num_congrats = len(res_list)
    res_data = {"congrats":res_list,
                "has_congrats": bool(num_congrats),
                "num_congrats": num_congrats}
    return Response(data=res_data, status=status.HTTP_200_OK)
        
        