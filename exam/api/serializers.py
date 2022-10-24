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
