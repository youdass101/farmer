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
    medium_weight = models.IntegerField()
    packweight = models.IntegerField()
    
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
    location = models.CharField(max_length=255)

    def __str__(self):
            return f"{self.name} start:{self.start}"

    def serialize(self):
        # TODAY DATE 
        today = datetime.today()
        # CALCULATE DAYS COUNT OF CREATED TRAY
        days = datetime.date(today) - datetime.date(self.start)
        # CALCULATE END DATE 
        end = datetime.date(self.start) + timedelta(self.name.harvest)
        try:
            # IF TRAY IS HARVESTED ALREADY COLLECT DATA
            h = Harvest.objects.get(tray=self)
            harvest_weight = h.output
            harvest = True
            harvest_date = h.date
            dh = h.date - datetime.date(self.start)
        except:
            # IF TRAY NOT HARVESTED AND STILL ACTIVE 
            harvest = False
            harvest_weight = None
            dh = None
            harvest_date = None
        return {
            # DATA TO RETURN FOR SERIALZATION 
            "fname": self.fname,
            "end": end,
            "days": days,
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "medium": self.medium,
            "start": datetime.date(self.start),
            "medium_weight": self.medium_weight,
            "seeds_weight": self.seeds_weight,
            "harvest" : harvest,
            "harvest_weight": harvest_weight,
            "dh" : dh,
            "harvest_date" : harvest_date,
            "location" : self.location
        }

class Harvest(models.Model):
    tray = models.ForeignKey(Tray, on_delete=models.CASCADE)
    date = models.DateField()
    output = models.IntegerField()


class BulkHarvest(models.Model):
    Product = models.ForeignKey(Plant, blank=True, null=True, on_delete=models.SET_NULL)
    MediumMix = models.ForeignKey(Medium, blank=True, null=True, on_delete=models.SET_NULL)
    Trays = models.IntegerField()
    Harvestdate = models.DateField()
    PacksQtt = models.IntegerField()
    PacksWeight = models.IntegerField()
    MixWeight = models.IntegerField()
    MediumWeightpacks = models.IntegerField()
    MediumWeightMix = models.IntegerField()
    SeedsWeightPacks = models.IntegerField()
    SeedsWeightMix = models.IntegerField()

    def serialize(self):
        # Total yield weight
        totalweight = self.PacksWeight + self.MixWeight
        totalmedium = self.MediumWeightpacks + self.MediumWeightMix
        totalseeds = self.SeedsWeightPacks + self.SeedsWeightMix

        return {
            # DATA TO RETURN FOR SERIALZATION 
            "product": self.Product,
            "medium": self.MediumMix,
            "trays_QTT": self.Trays,
            "date": self.Harvestdate,
            "packs_QTT": self.PacksQtt,
            "packs_weight": self.PacksWeight,
            "mix_weight": self.MixWeight,
            "total_weight": totalweight,
            "packs_medium": self.MediumWeightpacks,
            "mix_medium": self.MediumWeightMix,
            "total_medium" : totalmedium,
            "packs_seeds": self.SeedsWeightPacks,
            "mix_seeds" : self.SeedsWeightMix,
            "total_seeds" : totalseeds,
        }

    

    