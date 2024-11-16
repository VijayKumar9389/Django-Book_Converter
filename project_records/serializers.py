from rest_framework import serializers
from .models import ProjectRecord


# Serializer for the ProjectRecord model
class ProjectRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRecord
        fields = '__all__'
