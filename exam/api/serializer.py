from exam.models import *
from rest_framework import serializers
from django.urls import reverse

class TestSerializer(serializers.ModelSerializer):
    classroom_url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Test
        fields = "__all__"
    def get_classroom_url(self, obj):
        return reverse('classroom:classroom_detail', kwargs={'pk': obj.classroom.id})

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = McqOption
        fields = "__all__"

class AnswerSheetSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField(read_only=True)
    avatar_url = serializers.SerializerMethodField(read_only=True)
    answers_submitted = serializers.SerializerMethodField(read_only=True)
    answers_correct = serializers.SerializerMethodField(read_only=True)
    score = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AnswerSheet
        exclude = ['test', 'submit_time', 'user']

    def get_student_name(self, obj):
        return obj.user.account.user_full_name
    def get_avatar_url(self, obj):
        return obj.user.account.avatar_url
    def get_answers_submitted(self, obj):
        return obj.num_mcq_answers + obj.num_des_answers   
    def get_answers_correct(self, obj):
        return obj.num_correct_ans
    def get_score(self, obj):
        return obj.total_score 
