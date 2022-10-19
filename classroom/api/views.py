from rest_framework.generics import ListAPIView
from classroom.models import ClassroomPost
from .serializer import PostSerializer

class ClassroomPostsView(ListAPIView):
    serializer_class = PostSerializer
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        posts = ClassroomPost.objects.filter(classroom__id=pk)
        return posts
