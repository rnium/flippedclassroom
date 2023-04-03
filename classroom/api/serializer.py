from django.urls import reverse
from rest_framework import serializers
from classroom.models import ClassroomPost, Classroom, PostTopic, AssessmentMeta, Assessment


class PostTopicSerializer(serializers.ModelSerializer):
    topic_url = serializers.SerializerMethodField()
    class Meta:
        model = PostTopic
        fields = ['topic_url', 'name']
    def get_topic_url(self, obj):
        return reverse('classroom:topic_posts', kwargs={'pk':obj.classroom.id, 'topic_id':obj.str_id})


class PostSerializer(serializers.ModelSerializer):
    topics = PostTopicSerializer(read_only=True, many=True)
    view_url = serializers.SerializerMethodField()
    num_attachments = serializers.SerializerMethodField()
    num_comments = serializers.SerializerMethodField()
    action_permitted = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()
    class Meta:
        model = ClassroomPost
        exclude = ['author', 'classroom']

    def get_view_url(self, obj):
        return reverse('classroom:post_detail', kwargs={'pk':obj.id})

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

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if hasattr(request, 'user'):
            if request.user in obj.classroom.teachers.all():
                return reverse('classroom:edit_post', kwargs={'pk':obj.id})
            else:
                return None
        else:
            return None
    
    def get_delete_url(self, obj):
        request = self.context.get('request')
        if hasattr(request, 'user'):
            if request.user in obj.classroom.teachers.all():
                return reverse('classroom:delete_post', kwargs={'pk':obj.id})
            else:
                return None
        else:
            return None

class ClassroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['name', 'course', 'join_code', 'quote', 'active']

class AssessmentSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    registration = serializers.SerializerMethodField()
    pre_cls_points = serializers.SerializerMethodField()
    in_cls_points = serializers.SerializerMethodField()
    post_cls_points = serializers.SerializerMethodField()
    class Meta:
        model = Assessment
        exclude = ['meta', 'student']
    def get_student_name(self, obj):
        return obj.student.account.user_full_name
    def get_registration(self, obj):
        return obj.student.account.institutional_id
    def get_pre_cls_points(self, obj):
        return obj.pre_cls_points
    def get_in_cls_points(self, obj):
        return obj.in_cls_points
    def get_post_cls_points(self, obj):
        return obj.post_cls_points

class AssessmentMetaSerializer(serializers.ModelSerializer):
    assessments = AssessmentSerializer(many=True, read_only=True)
    class Meta:
        model = AssessmentMeta
        exclude = ['id', 'classroom']

        