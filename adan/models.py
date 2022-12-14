from django.db import models

# Create your models here.

class LiveEvent(models.Model):
    audio = models.FileField("audio file")

    def __str__(self):
        return self.id