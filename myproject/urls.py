from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('project.urls')),  # This includes the 'projects' URL
    path('api/', include('project_records.urls')),  # This includes the 'project_records' URL
    path('api/', include('utilities.urls')),  # This includes the 'utilities' URL

    path('api/', include('authentication.urls')),  # This includes the 'authentication' URL

]
