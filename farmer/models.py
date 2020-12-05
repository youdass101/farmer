from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
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
    number = models.IntegerField()
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    start = models.DateTimeField()
    medium_weight = models.IntegerField()
    seeds_weight = models.IntegerField()
    fname = models.CharField(max_length=255)

    def __str__(self):
            return f"{self.name} start:{self.start}"

    def serialize(self):
        today = datetime.today()
        days = datetime.date(today) - datetime.date(self.start)
        end = datetime.date(self.start) + timedelta(self.name.harvest)
        try:
            h = Harvest.objects.get(tray=self)
            harvest_weight = h.output
            harvest = True
            harvest_date = h.date
            dh = h.date - datetime.date(self.start)
        except:
            harvest = False
            harvest_weight = None
            dh = None
            harvest_date = None
        return {
            "fname": self.fname,
            "end": end,
            "days": days,
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "medium": self.medium,
            "date" : self.start,
            "start": datetime.date(self.start),
            "medium_weight": self.medium_weight,
            "seeds_weight": self.seeds_weight,
            "harvest" : harvest,
            "harvest_weight": harvest_weight,
            "dh" : dh,
            "harvest_date" : harvest_date
        }

class Harvest(models.Model):
    tray = models.ForeignKey(Tray, on_delete=models.CASCADE)
    date = models.DateField()
    output = models.IntegerField()

    