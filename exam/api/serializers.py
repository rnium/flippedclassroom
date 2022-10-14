from exam.models import *
from rest_framework.serializers import ModelSerializer

class TestSerializer(ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"

class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"

class OptionSerializer(ModelSerializer):
    class Meta:
        model = McqOption
        fields = "__all__"
