from django.db import models

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
        return 
