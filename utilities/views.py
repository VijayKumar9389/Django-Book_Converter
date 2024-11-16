import xlsxwriter
import logging
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from project.models import Project
from project_records.models import ProjectRecord, ProjectRecordCompleted
from rest_framework.decorators import api_view

logger = logging.getLogger(__name__)

@api_view(['GET'])
def compare_and_export_records(request, project_id):
    try:
        # Retrieve the project using the provided project_id
        project = Project.objects.get(id=project_id)

        # Retrieve project records and completed project records
        project_records = ProjectRecord.objects.filter(project=project)
        completed_project_records = ProjectRecordCompleted.objects.filter(project=project)

        # Create a new workbook and add a worksheet
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="project_comparison_{project_id}.xlsx"'

        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet("Project Record Comparison")

        # Define red font and strikethrough format
        red_format = workbook.add_format({'font_color': 'red'})
        strikethrough_format = workbook.add_format({'font_strikeout': True})

        # Define headers for the Excel file (excluding "Position")
        headers = [
            "Tract", "Pin", "Structure", "Interest", "Status", "Name",
            "Street Address", "Mailing Address", "Phone Number", "Occupants", "Works Land",
            "Contacted", "Attempts", "Consultation", "Follow Up", "Comments", "Email",
            "Commodity", "Pipeline Status", "Page No", "Keep/Delete"
        ]

        # Write headers to the worksheet
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header)

        # Mapping of Excel headers to model fields for comparison (case-sensitive and exact match)
        field_mapping = {
            "Tract": "tract",
            "Pin": "pin",
            "Structure": "structure",
            "Interest": "interest",
            "Status": "status",
            "Name": "name",
            "Street Address": "street_address",  # Ensure this matches the model's field name
            "Mailing Address": "mailing_address",  # Ensure this matches the model's field name
            "Phone Number": "phone_number",  # Ensure this matches the model's field name
            "Occupants": "occupants",
            "Works Land": "works_land",  # Ensure this matches the model's field name
            "Contacted": "contacted",
            "Attempts": "attempts",
            "Consultation": "consultation",
            "Follow Up": "follow_up",
            "Comments": "comments",
            "Email": "email",
            "Commodity": "commodity",
            "Pipeline Status": "pipeline_status",
            "Page No": "page_no",
        }

        # Map positions of project records for easy comparison
        project_record_dict = {record.position: record for record in project_records}
        completed_record_dict = {record.position: record for record in completed_project_records}

        # Compare records and populate the sheet
        row_number = 1  # Start from the second row (first row is for headers)
        for position, record in project_record_dict.items():
            completed_record = completed_record_dict.get(position)

            if completed_record:
                # Compare each field in the record and populate the row
                for col_num, header in enumerate(headers):  # Iterate over all fields except 'Position'
                    model_field = field_mapping.get(header, None)

                    if model_field:
                        project_value = getattr(record, model_field, '')  # Access model fields dynamically
                        completed_value = getattr(completed_record, model_field, '')

                        # Compare the values and write with formatting
                        if project_value != completed_value:
                            if completed_value == '':
                                # If completed value is empty, apply strikethrough to the old value
                                worksheet.write_rich_string(row_number, col_num, strikethrough_format,
                                                            str(project_value))
                            else:
                                # If values are different, highlight the new value in red and old value with strikethrough
                                worksheet.write_rich_string(row_number, col_num,
                                                            red_format, str(completed_value),
                                                            strikethrough_format, ' ' + str(project_value))
                        else:
                            # If the values are the same, just write the original value
                            worksheet.write(row_number, col_num, str(project_value))

                row_number += 1

        # Close the workbook to write to the response
        workbook.close()

        return response

    except Project.DoesNotExist:
        logger.error(f"Project with ID {project_id} not found.")
        return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error occurred while comparing records: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
