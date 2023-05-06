from rest_framework import serializers

from src.cases.models import CaseModel, TaskModel


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseModel
        fields= "__all__"


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields= "__all__"
