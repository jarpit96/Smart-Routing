from __future__ import unicode_literals

from django.db import models
import datetime
# Create your models here.

class State (models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class District(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    def __str__(self):
        return self.name
class Locality(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=400)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    crime_wt = models.FloatField(default=0)
    poi_wt = models.FloatField(default=3)
    traffic_wt = models.FloatField(default=3)
    lat = models.FloatField()
    lng = models.FloatField()
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name