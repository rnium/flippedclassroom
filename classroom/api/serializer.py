from symtable import Class
from rest_framework import serializers
from classroom.models import ClassroomPost

class PostSerializer(serializers.ModelSerializer):
    num_attachments = serializers.SerializerMethodField()
    class Meta:
        model = ClassroomPost
        exclude = ['author', 'classroom']
    def get_num_attachments(self, obj):
        return obj.postattachment_set.count()
        