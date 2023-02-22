from django.db import models
from django.contrib.auth.models import User
import json
import mutagen
from constance import config
from datetime import datetime, timedelta
PRAYER= (('elfajer','elfajer'),('duhr','duhr'),('alasr','alasr'),('almaghreb','almaghreb'),('alaicha','alaicha'))

class PrayerAudio(models.Model):
    audio = models.FileField("audio file")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(PrayerAudio, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return self.prayer

class LiveEvent(models.Model):
    """This event is triggered immediately"""
    audio = models.FileField("audio file")
    name = models.CharField( max_length=120,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(LiveEvent, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return str(self.name) if self.name else f"audio--{self.id}"
class State(models.Model):
    name = models.CharField("state name", max_length=120)
    offset_time = models.IntegerField()
    prayer_time = models.JSONField("prayer data time",null=True,blank=True)
    prayer_time_am_pm = models.JSONField("prayer data time with am pm",null=True,blank=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        prayer_source=json.loads(config.PRAYER_SOURCE)["data"]
        new_dictionary = {"data":[]}
        for prayer in prayer_source :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M')+timedelta(minutes=self.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary["data"].append(new_dictionary_item)
            self.prayer_time=new_dictionary
        prayer_source_am_pm=json.loads(config.PRAYER_SOURCE_AM_PM)["data"]
        new_dictionary_am_pm = {"data":[]}
        for prayer in prayer_source_am_pm :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M %p')+timedelta(minutes=self.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary_am_pm["data"].append(new_dictionary_item)
            self.prayer_time_am_pm=new_dictionary_am_pm
        super(State, self).save(*args, **kwargs) # Call the real save() method

class PrayerEvent(models.Model):
    TYPE = (('after','after'),('before','before'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=TYPE)
    name = models.CharField(max_length=120,null=True)
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio = models.FileField(upload_to="prayer_event", max_length=250,null=True,blank=True)
    audio_duration = models.PositiveIntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
       if self.audio_duration is None or self.audio_duration == "":
        audio_info = mutagen.File(self.audio).info
        self.audio_duration=int(audio_info.length)
       super(PrayerEvent, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return f"{self.type}-{self.prayer}"


class Plug(models.Model):
    topic = models.ForeignKey('adan.mosque', on_delete=models.CASCADE)
    name = models.CharField(max_length=120,blank=True, null=True)
    state = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} - {self.topic}"


class Mosque(models.Model):
    topic = models.OneToOneField('adan.topic', on_delete=models.CASCADE,null=True)
    name = models.CharField("name of mosque", max_length=150,null=True)
    speaker_status = models.BooleanField(default=False,help_text="speaker status")
    status = models.BooleanField(default=False,help_text="raspbery pi status")
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f"{self.name}"

class Topic(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    serial_number = models.CharField(max_length=300,unique=True)
    name = models.CharField(max_length=120,null=True,blank=True)
    def __str__(self):
        topic = f" {self.serial_number} || {self.name} "
        return  topic
