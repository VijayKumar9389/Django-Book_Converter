from django.db import models

# Project model
class Project(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return self.name