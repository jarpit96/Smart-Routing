from __future__ import unicode_literals

from django.db import models


# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200, null=True)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Locality(models.Model):
    name = models.CharField(max_length=400, null=True)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    crime_wt = models.FloatField(default=0.0)
    poi_wt = models.FloatField(default=0.0)
    traffic_wt = models.FloatField(default=0.0)
    lat = models.FloatField(default=0.0)
    lng = models.FloatField(default=0.0)

    def __str__(self):
        return self.name