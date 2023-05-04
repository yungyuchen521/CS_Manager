from rest_framework import serializers

from src.cases.models import CaseModel


class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseModel
        fields= "__all__"
