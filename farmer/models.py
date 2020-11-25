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
        return f"{self.name} "

class Medium(models.Model):
    name = models.CharField(max_length=255)
    soil = models.IntegerField()
    coco = models.IntegerField()

    def __str__(self):
        return f"{self.name}"

class Tray(models.Model):
    name = models.ForeignKey(Plant, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    start = models.DateTimeField(auto_now_add=True)
    medium_weight = models.IntegerField()
    seeds_weight = models.IntegerField()

   

    def __str__(self):
        return f"{self.name} start:{self.start}"