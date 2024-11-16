from django.urls import path
from .views import create_project, view_all_projects

urlpatterns = [
    path('projects/', view_all_projects, name='view_all_projects'),
    path('projects/create/', create_project, name='create_project'),
]