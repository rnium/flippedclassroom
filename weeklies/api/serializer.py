from dataclasses import fields
from weeklies.models import Weekly
from rest_framework import serializers

class WeeklySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekly
        fields = "__all__"
        