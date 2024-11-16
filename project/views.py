import logging
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Project
from project_records.models import ProjectRecord
from .serializers import ProjectSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def create_project(request):
    try:
        # Ensure the required fields are in the request data
        project_data = request.data
        project_name = project_data.get('name')
        project_year = project_data.get('year')
        project_notes = project_data.get('notes')

        if not project_name:
            return Response({"error": "Project name is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Create the project instance
        project = Project.objects.create(
            name=project_name,
            year=project_year,
            notes=project_notes
        )

        # Get project records from request, or default to an empty list
        project_records = project_data.get('projectRecords', [])

        if project_records:  # Only create records if there are any
            for record in project_records:
                ProjectRecord.objects.create(
                    project=project,
                    position=record.get('position', 0),
                    tract=record.get('tract', 0),
                    pin=record.get('pin', ''),
                    structure=record.get('structure', ''),
                    interest=record.get('interest', ''),
                    status=record.get('status', ''),
                    name=record.get('name', ''),
                    street_address=record.get('streetAddress', ''),
                    mailing_address=record.get('mailingAddress', ''),
                    phone_number=record.get('phoneNumber', ''),
                    occupants=record.get('occupants', 0),
                    works_land=record.get('worksLand', ''),
                    contacted=record.get('contacted', ''),
                    attempts=record.get('attempts', ''),
                    consultation=record.get('consultation', ''),
                    follow_up=record.get('followUp', ''),
                    comments=record.get('comments', ''),
                    email=record.get('email', ''),
                    commodity=record.get('commodity', ''),
                    pipeline_status=record.get('pipelineStatus', ''),
                    page_no=record.get('pageNo', ''),
                    keep_delete=record.get('keepDelete', ''),
                )

        return Response({"message": "Project and records created successfully"}, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error occurred while creating project: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def view_all_projects(request):
    try:
        # Retrieve all projects
        projects = Project.objects.all()

        # Pass the queryset to the serializer and specify many=True
        serializer = ProjectSerializer(projects, many=True)

        # Ensure the response data is serialized and returned as JSON
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error occurred while retrieving projects: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
