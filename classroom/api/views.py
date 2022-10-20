from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from classroom.models import ClassroomPost, Classroom
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
