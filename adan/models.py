from django.db import models
from django.contrib.auth.models import User
import json
from django.core.serializers.json import DjangoJSONEncoder

from constance import config
from datetime import datetime, timedelta
class LiveEvent(models.Model):
    """This event is triggered immediately"""
    audio = models.FileField("audio file")
    created_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.id

class State(models.Model):
    name = models.CharField("state name", max_length=120)
    offset_time = models.IntegerField()
    def __str__(self):
        return self.name

class Prayer(models.Model):
    """ Prayer (salat) ``model`` """
    state = models.ForeignKey("adan.state", on_delete=models.CASCADE)
    prayer_time = models.JSONField("prayer data time",null=True,blank=True)
    def __str__(self):
        return self.state.name
    def save(self, *args, **kwargs):
       if self.prayer_time is None or self.prayer_time=="":
        prayer_source=json.loads(config.PRAYER_SOURCE)["data"]
        new_dictionary = {"data":[]}
        for prayer in prayer_source :
            elfajer=(datetime.strptime(prayer["elfajer"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            duhr=(datetime.strptime(prayer["duhr"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            alasr=(datetime.strptime(prayer["alasr"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            almaghreb=(datetime.strptime(prayer["almaghreb"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            alaicha=(datetime.strptime(prayer["alaicha"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            chorouk=(datetime.strptime(prayer["chorouk"], '%H:%M %p')+timedelta(minutes=self.state.offset_time)).time()
            new_dictionary_item = {"id":prayer["id"],"date":prayer["date"],"elfajer":str(elfajer),"chorouk":str(chorouk),"duhr":str(duhr),"alasr":str(alasr),"almaghreb":str(almaghreb),"alaicha":str(alaicha)}
            new_dictionary["data"].append(new_dictionary_item)
            self.prayer_time=new_dictionary
            print(alasr)
       super(Prayer, self).save(*args, **kwargs) # Call the real save() method
class PrayerEvent(models.Model):
    TYPE = (('after','after'),('before','before'))
    PRAYER= (('elfajer','elfajer'),('duhr','duhr'),('alasr','alasr'),('almaghreb','almaghreb'),('alaicha','alaicha'))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,choices=TYPE)
    repeated = models.BooleanField(default=True)
    prayer = models.CharField(max_length=50,choices=PRAYER)
    audio = models.FileField(upload_to="prayer_event", max_length=250,null=True,blank=True)
    def __str__(self):
        return f"{self.type}-{self.prayer}"

class Mosque(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField("name of mosque", max_length=150)
    status = models.BooleanField(default=False)
    state = models.ForeignKey(State, on_delete=models.CASCADE,null=True,blank=True)
    prayer = models.JSONField(null=True,blank=True)
    def save(self, *args, **kwargs):
        if self.prayer is None or self.prayer=="":
            self.prayer=Prayer.objects.filter(state=self.state).first()
        super(Mosque, self).save(*args, **kwargs) # Call the real save() method
    def __str__(self):
        return f"{self.name} is {self.status} now"
