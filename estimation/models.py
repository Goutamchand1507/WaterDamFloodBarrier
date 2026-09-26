from django.db import models
from projects.models import Project
from materials.models import Material


class Estimation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)

    water_level = models.FloatField()
    ground_level = models.FloatField()
    safety_allowance = models.FloatField()

    barrier_length = models.FloatField()
    barrier_width = models.FloatField()
    barrier_height = models.FloatField()
    barrier_volume = models.FloatField()

    material_quantity = models.FloatField()
    material_cost = models.FloatField()
    labour_cost = models.FloatField()
    equipment_cost = models.FloatField()
    transportation_cost = models.FloatField()
    other_cost = models.FloatField()

    total_cost = models.FloatField()

    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_name} - Estimation"