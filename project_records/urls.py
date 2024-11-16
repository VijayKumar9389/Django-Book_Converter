from django.urls import path
from .views import view_project_records, create_completed_project_records, delete_all_completed_project_records, view_completed_project_record

urlpatterns = [
    path('projects/<int:project_id>/', view_project_records, name='view_project_records'),
    path('projects/completed-records/<int:project_id>/', create_completed_project_records,
         name='create_completed_project_records'),
    path('projects/completed-records/delete/<int:project_id>', delete_all_completed_project_records,
         name='delete_completed_project_records'),
    path('projects/completed-records/<int:project_id>/<int:position>/', view_completed_project_record,
         name='view_completed_project_record'),
]
