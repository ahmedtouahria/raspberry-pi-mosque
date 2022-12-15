from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class LiveEvent(models.Model):
    """This event is triggered immediately"""
    audio = models.FileField("audio file")
    def __str__(self):
        return self.id

class State(models.Model):
    name = models.CharField("state name", max_length=120)
    def __str__(self):
        return self.name

class Prayer(models.Model):
    state = models.ForeignKey("adan.state", on_delete=models.CASCADE)
    prayer_time = models.JSONField("prayer data time")
    def __str__(self):
        return self.state

class PrayerEvent(models.Model):
    TYPE = (('after','after'),('before','before'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=TYPE)
    repeated = models.BooleanField(default=True)
    prayer = models.CharField(max_length=50)
    def __str__(self):
        return 
