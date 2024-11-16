from django.urls import path
from utilities.views import compare_and_export_records


urlpatterns = [
    path('projects/compare/<int:project_id>/', compare_and_export_records, name='compare_and_export_records'),
]