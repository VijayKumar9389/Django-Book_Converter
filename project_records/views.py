from project_records.serializers import ProjectRecordSerializer
import logging
from rest_framework.response import Response
from rest_framework import status
from project.models import Project
from project_records.models import ProjectRecord, ProjectRecordCompleted
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)


@api_view(['DELETE'])
def delete_all_completed_project_records(request, project_id):
    try:
        # Retrieve the project using the provided project_id
        project = Project.objects.get(id=project_id)

        # Delete all completed project records associated with the project
        records_deleted, _ = ProjectRecordCompleted.objects.filter(project=project).delete()

        if records_deleted == 0:
            return Response({"message": "No completed project records found to delete."},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"message": f"{records_deleted} completed project records deleted successfully."},
                        status=status.HTTP_204_NO_CONTENT)

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error occurred while deleting completed project records: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_completed_project_records(request, project_id):
    try:
        # Retrieve the project using the provided project_id
        project = Project.objects.get(id=project_id)

        # Check if there are any completed project records already in the database for this project
        existing_records = ProjectRecordCompleted.objects.filter(project=project)

        if existing_records.exists():
            return Response({"error": "Completed project records already exist for this project."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Ensure the required data is in the request
        completed_project_records = request.data.get('completedProjectRecords', [])

        if not completed_project_records:
            return Response({"error": "Completed project records are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Loop through the records and create the ProjectRecordCompleted instances
        for record in completed_project_records:
            ProjectRecordCompleted.objects.create(
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

        return Response({"message": "Completed project records added successfully"}, status=status.HTTP_201_CREATED)

    except Project.DoesNotExist:
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error occurred while creating completed project records: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def view_project_records(request, project_id):
    try:
        # Check if project_id is valid
        if not project_id:
            logger.error(f"Invalid project ID: {project_id}")
            return Response({"error": "Invalid project ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the project using the provided ID
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            logger.error(f"Project with ID {project_id} not found.")
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve all project records associated with this project
        project_records = ProjectRecord.objects.filter(project=project)

        # Serialize the project records
        serializer = ProjectRecordSerializer(project_records, many=True)

        # Return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the error for debugging
        logger.error(f"Error occurred while retrieving project records for project ID {project_id}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# get completed project record by project id and position
@api_view(['GET'])
def view_completed_project_record(request, project_id, position):
    try:
        # Check if project_id is valid
        if not project_id:
            logger.error(f"Invalid project ID: {project_id}")
            return Response({"error": "Invalid project ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the project using the provided ID
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            logger.error(f"Project with ID {project_id} not found.")
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve the completed project record by project ID and position
        completed_project_record = ProjectRecordCompleted.objects.filter(project=project, position=position)

        # Serialize the completed project record
        serializer = ProjectRecordSerializer(completed_project_record, many=True)

        # Return serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the error for debugging
        logger.error(
            f"Error occurred while retrieving completed project record for project ID {project_id} and position {position}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
