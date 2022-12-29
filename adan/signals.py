from mqtt import mqtt_publisher
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
 
 
@receiver(post_save, sender=LiveEvent)
def create_live_event(sender, instance, **kwargs):
    json_msg={
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "LiveEvent",
		"name": instance.name,
		"user": instance.user.id,
		"audio": instance.audio.url,
		#"audio": "http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/intromusic.ogg",
		"audio_duration": instance.audio_duration
	}}   
    #print(instance.user.topic)
    self_topic=instance.user.topic
    json_msg_publisher=json.dumps(json_msg,ensure_ascii=False)  #ensure_ascii for decode arabic characters
    mqtt_publisher.main(topic=self_topic, message=json_msg_publisher)

@receiver(post_save, sender=PrayerEvent)
def create_after_before_event(sender, instance, **kwargs):
    json_msg={
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "PrayerEvent",
		"type": instance.type,
		"name": instance.name,
		"user": instance.user.id,
		"repeated": instance.repeated,
		"prayer": instance.prayer,
		"audio": instance.audio.url,
		"audio_duration": instance.audio_duration
	}}   
    #print(instance.user.topic)

    json_msg_publisher=json.dumps(json_msg,ensure_ascii=False)  #ensure_ascii for decode arabic characters
    mqtt_publisher.main(topic=str(instance.user.topic), message=json_msg_publisher)



@receiver(post_save, sender=PrayerAudio)
def create_prayer_audio(sender, instance, **kwargs):
    json_msg={
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "PrayerAudio",
		"prayer": instance.prayer,
		"user": instance.user.id,
		"audio": instance.audio.url,
		"audio_duration": instance.audio_duration
	}}   
    json_msg_publisher=json.dumps(json_msg,ensure_ascii=False)  #ensure_ascii for decode arabic characters
    mqtt_publisher.main(topic=str(instance.user.topic), message=json_msg_publisher)


