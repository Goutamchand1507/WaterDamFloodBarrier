from django.db import models


class Material(models.Model):
    material_name = models.CharField(max_length=100)
    density = models.FloatField()
    unit = models.CharField(max_length=50)
    unit_price = models.FloatField()

    def __str__(self):
        return self.material_name