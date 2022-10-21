from rest_framework import serializers
from classroom.models import ClassroomPost

class PostSerializer(serializers.ModelSerializer):
    num_attachments = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    action_permitted = serializers.SerializerMethodField()
    class Meta:
        model = ClassroomPost
        exclude = ['author', 'classroom']

    def get_num_attachments(self, obj):
        return obj.num_attachments

    def get_num_comments(self, obj):
        return obj.num_comments

    def get_action_permitted(self, obj):
        request = self.context.get('request')
        if hasattr(request, 'user'):
            if request.user in obj.classroom.teachers.all():
                return True
            else:
                return False
        else:
            return False
        