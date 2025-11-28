from django.db import models

# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(TimeStampedModel):
    name = models.CharField(max_length=200, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation_m = models.FloatField(null=True, blank=True)
    locality = models.CharField(max_length=120, blank=True)  # village/town/city
    region = models.CharField(max_length=120, blank=True)  # district/state
    country_code = models.CharField(max_length=2, blank=True)  # ISO-3166-1 alpha-2 eg:"IN"
    tz = models.CharField(max_length=64, blank=True)  # "Asia/Kolkata"

    class Meta:
        unique_together = ("latitude", "longitude")
        indexes = [
            models.Index(fields=["latitude", "longitude"]),
            models.Index(fields=["country_code", "region"]),
        ]

    def __str__(self) -> str:
        return self.name or f"{self.latitude},{self.longitude}"
    

class Farm(TimeStampedModel):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200,blank=True)
    contact_phone = models.CharField(max_length=40,blank=True)
    home_location = models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,blank=True,related_name="farms")

    class Meta:
        indexes = [models.Index(fields=["name"])]

    def __str__(self) -> str:
        return self.name


class FieldPlot(TimeStampedModel):

    IRRIGATION_CHOICES = [
        ("none","None"),
        ("drip","Drip"),
        ("sprinkler","Sprinkler"),
        ("flood","Flood"),
    ]

    farm = models.ForeignKey(Farm,on_delete=models.CASCADE,related_name="fields")
    name = models.CharField(max_length=120)
    area_ha = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    centroid_lat = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    centroid_lon = models.DecimalField(max_digits=9,decimal_places=6,null=True,blank=True)
    boundary_geo = models.JSONField(null=True,blank=True)
    soil_type = models.CharField(max_length=120,blank=True) #loam,clay
    soil_ph = models.FloatField(null=True,blank=True)
    irrigation_type = models.CharField(max_length=20,choices=IRRIGATION_CHOICES,default="none")
    default_rain_alert_mm = models.FloatField(null=True,blank=True) # threshold for alert
    
    class Meta:
        unique_together = ("farm","name")
        indexes = [models.Index(fields=["farm"])]
    
    def __str__(self) -> str:
        return f"{self.farm.name} - {self.name}"


class Crop(TimeStampedModel):
    name = models.CharField(max_length=120) # maize.rice,wheat
    scientific_name = models.CharField(max_length=200,blank=True)
    category = models.CharField(max_length=120,blank=True) # cereal, etc..

    class Meta:
        unique_together = ("name", "scientific_name")

    def __str__(self) -> str:
        return self.name
