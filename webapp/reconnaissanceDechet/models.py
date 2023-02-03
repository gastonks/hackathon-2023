from django.db import models

class MarkeurMap(models.Model):
    name = models.CharField(max_length=300)
    latitude = models.IntegerField()
    longitude = models.IntegerField()