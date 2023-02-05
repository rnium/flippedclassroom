from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from classroom.models import ClassroomPost, PostAttachment, Classroom, Comment, AssessmentMeta, Assessment
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
        return Classroom.objects.filter(pk=self.kwargs.get('pk'))

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
    serializer = ClassroomSerializer(data=request.data)
    if serializer.is_valid():
        classroom = serializer.save()
        classroom.teachers.add(request.user)
        response_data = {}
        response_data['name'] = classroom.name
        response_data['classroom_url'] = reverse("classroom:classroom_detail", args=(classroom.id,))
        response_data["join_link"] = request.build_absolute_uri(reverse("classroom:join_classroom", args=(classroom.id,)))
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        return Response(data={"status":"error"}, status=status.HTTP_400_BAD_REQUEST)

 
@api_view(['POST'])
@permission_classes([IsAuthenticated & IsUserPartOfClassroom])
def remove_student(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    try:
        user_id = request.data['user_id']
    except KeyError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    student = get_object_or_404(User, pk=user_id)
    if (request.user in classroom.teachers.all()) or (request.user==student):
        classroom.students.remove(student)
        return Response({'status':"user removed"}, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
    

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