from django.db import models


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name