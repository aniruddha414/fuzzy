from django.db import models

# Create your models here.
class Ac(models.Model):
    
    temperature = models.FloatField()
    humidity = models.IntegerField()
    power = models.FloatField()

class Rule(models.Model):

    temperature = models.CharField(max_length = 2)
    humidity = models.CharField(max_length = 2)
    power = models.CharField(max_length = 2)

