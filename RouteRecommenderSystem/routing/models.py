from __future__ import unicode_literals

from django.db import models


# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=200)


class District(models.Model):
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=models.CASCADE)


class Locality(models.Model):
    name = models.CharField(max_length=400)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    crime_wt = models.FloatField()
    poi_wt = models.FloatField()
    traffic_wt = models.FloatField()
    lat = models.FloatField()
    lng = models.FloatField()
