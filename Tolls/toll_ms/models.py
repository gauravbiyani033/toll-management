from django.db import models

VEHICLE_TYPES = (
    ('0', "TWO_WHEELER"),
    ('1', "FOUR_WHEELER")
)

PASS_TYPES = (
    ('0', "single"),
    ('1', 'return'),
    ('2', 'seven days'),
)

# Create your models here.
class Toll(models.Model):
    pid = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    vehicles_processed = models.IntegerField(default=0)
    charges_collected = models.IntegerField(default=0)

class TollPriceDetails(models.Model):
    toll = models.ForeignKey(Toll, on_delete=models.CASCADE)
    vehicle_type = models.CharField(
        max_length = 20,
        choices=VEHICLE_TYPES,
    )   
    single_pass = models.FloatField()
    return_pass = models.FloatField()
    seven_day_pass = models.FloatField()

class Vehicle(models.Model):
    registration_num = models.CharField(max_length=10)
    pid = models.CharField(max_length=30)
    type = models.CharField(
        max_length = 20,
        choices=VEHICLE_TYPES,
    )

class VehiclePass(models.Model):
    toll_pid = models.UUIDField()
    vehicle = models.ForeignKey(Vehicle, related_name = 'vehicle_passes', on_delete=models.CASCADE)  
    pass_type = models.CharField(
        max_length = 20,
        choices=PASS_TYPES,
    )
    is_valid = models.BooleanField(default=True)   

class VehicleProcessed(models.Model):
    toll_pid = models.UUIDField()
    vehicle_pid = models.UUIDField()
    charge = models.FloatField()
