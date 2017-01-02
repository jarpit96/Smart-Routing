from __future__ import unicode_literals

from django.db import models
import datetime


# Create your models here.

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class District(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    state = models.ForeignKey('State', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Locality(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=400)
    district = models.ForeignKey('District', on_delete=models.CASCADE)
    crime_wt = models.FloatField(default=0)
    #poi_wt = models.FloatField(default=3)
    poi = models.ForeignKey('PointOfInterests', on_delete=models.CASCADE, null=True)
    traffic_wt = models.FloatField(default=3)
    lat = models.FloatField()
    lng = models.FloatField()
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name


class PointOfInterests(models.Model):
    amusement_park_wt = models.FloatField(default=3.0)
    art_gallery_wt = models.FloatField(default=3.0)
    cafe_wt = models.FloatField(default=3.0)
    casino_wt = models.FloatField(default=3.0)
    hindu_temple_wt = models.FloatField(default=3.0)
    zoo_wt = models.FloatField(default=3.0)
    spa_wt = models.FloatField(default=3.0)
    restaurant_wt = models.FloatField(default=3.0)
    museum_wt = models.FloatField(default=3.0)
    lodging_wt = models.FloatField(default=3.0)
