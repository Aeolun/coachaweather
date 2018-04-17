from django.db import models

# Create your models here.
class Tile(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    elevation = models.IntegerField()
    base_ice = models.IntegerField()
    base_water = models.IntegerField()

class Map(models.Model):
    name = models.TextField()

class CurrentTile(models.Model):
    map = models.ForeignKey(Map, models.CASCADE, related_name="tiles")

    x = models.IntegerField()
    y = models.IntegerField()
    elevation = models.IntegerField()
    current_ice = models.IntegerField()
    current_water = models.IntegerField()
    current_low_clouds = models.IntegerField()
    current_high_clouds = models.IntegerField()
    current_rain = models.IntegerField()
