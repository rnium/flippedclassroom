from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from classroom.models import ClassroomPost, Classroom, Comment
from .serializer import PostSerializer
from .permission import IsUserPartOfClassroom
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


@api_view(['POST'])
@permission_classes([IsAuthenticated & IsUserPartOfClassroom])
def post_comment(request, pk):
    try:
        post = ClassroomPost.objects.get(pk=pk)
    except Classroom.DoesNotExist:
        return Response({'status':'post not found'}, status=status.HTTP_404_NOT_FOUND)
    parent_comment = request.data.get('parent_comment_id')
    if parent_comment != None:
        try:
            parent = Comment.objects.get(pk=parent_comment)
        except Classroom.DoesNotExist:
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
    payload = {
        "parent_id": parent_comment,
        "id": comment.id,
        "author_name": comment.author.account.user_full_name,
        "avatar_url": comment.author.account.avatar_url,
        "cssClass": comment.cssClass,
        "comment_text": comment.comment_text,
        "comment_time": comment.comment_time,
        "num_comments": comment.post.num_comments,
    }

    return Response(payload, status=status.HTTP_201_CREATED)
