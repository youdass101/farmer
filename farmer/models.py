from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.conf import settings

class User(AbstractUser):
    pass

    def __str__(self):
        return f"Username: {self.username}"

class Plant(models.Model):
    name = models.CharField(max_length=255)
    seeds = models.IntegerField()
    pressure = models.IntegerField()
    blackout = models.IntegerField()
    harvest = models.IntegerField()
    output = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} seeds:{self.seeds}g pressure:{self.pressure}days blackout:{self.blackout}days harvest:{self.harvest}days output:{self.output}g"

class Medium(models.Model):
    name = models.CharField(max_length=255)
    soil = models.IntegerField()
    coco = models.IntegerField()

    def __str__(self):
        return f"{self.name} soil:{self.soil}% coco:{self.coco}%"