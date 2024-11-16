from rest_framework import serializers
from project.models import Project
from project_records.serializers import ProjectRecordSerializer


# Serializer for the ProjectRecord model
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'year', 'notes']


# Serializer for the Project model that includes the related project records
class ProjectWithRecordsSerializer(serializers.ModelSerializer):
    project_records = ProjectRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'year', 'notes', 'project_records']
