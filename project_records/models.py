from django.db import models
from project.models import Project

# Create your models here.
class ProjectRecord(models.Model):
    project = models.ForeignKey(Project, related_name='project_records', on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    tract = models.IntegerField()
    pin = models.CharField(max_length=500)  # Increased to 500
    structure = models.CharField(max_length=500)  # Increased to 500
    interest = models.CharField(max_length=500)  # Increased to 500
    status = models.CharField(max_length=500)  # Increased to 500
    name = models.CharField(max_length=500)  # Increased to 500
    street_address = models.CharField(max_length=500)  # Increased to 500
    mailing_address = models.CharField(max_length=500)  # Increased to 500
    phone_number = models.CharField(max_length=500)  # Increased to 500
    occupants = models.IntegerField()
    works_land = models.CharField(max_length=500)  # Increased to 500
    contacted = models.CharField(max_length=500)  # Increased to 500
    attempts = models.CharField(max_length=500)  # Increased to 500
    consultation = models.CharField(max_length=500)  # Increased to 500
    follow_up = models.CharField(max_length=500)  # Increased to 500
    comments = models.TextField()  # No change, as TextField already supports large content
    page_no = models.CharField(max_length=500)  # Increased to 500
    keep_delete = models.CharField(max_length=500)  # Increased to 500
    email = models.CharField(max_length=500)  # Increased to 500
    commodity = models.CharField(max_length=500)  # Increased to 500
    pipeline_status = models.CharField(max_length=500)  # Increased to 500

    def __str__(self):
        return f"ProjectRecord {self.tract} - {self.pin}"


class ProjectRecordCompleted(models.Model):
    project = models.ForeignKey(Project, related_name='completed_project_records', on_delete=models.CASCADE)
    position = models.IntegerField(default=0)
    tract = models.IntegerField()
    pin = models.CharField(max_length=500)  # Increased to 500
    structure = models.CharField(max_length=500)  # Increased to 500
    interest = models.CharField(max_length=500)  # Increased to 500
    status = models.CharField(max_length=500)  # Increased to 500
    name = models.CharField(max_length=500)  # Increased to 500
    street_address = models.CharField(max_length=500)  # Increased to 500
    mailing_address = models.CharField(max_length=500)  # Increased to 500
    phone_number = models.CharField(max_length=500)  # Increased to 500
    occupants = models.IntegerField()
    works_land = models.CharField(max_length=500)  # Increased to 500
    contacted = models.CharField(max_length=500)  # Increased to 500
    attempts = models.CharField(max_length=500)  # Increased to 500
    consultation = models.CharField(max_length=500)  # Increased to 500
    follow_up = models.CharField(max_length=500)  # Increased to 500
    comments = models.TextField()  # No change, as TextField already supports large content
    page_no = models.CharField(max_length=500)  # Increased to 500
    keep_delete = models.CharField(max_length=500)  # Increased to 500
    email = models.CharField(max_length=500)  # Increased to 500
    commodity = models.CharField(max_length=500)  # Increased to 500
    pipeline_status = models.CharField(max_length=500)  # Increased to 500

    def __str__(self):
        return f"ProjectRecord {self.tract} - {self.pin}"
