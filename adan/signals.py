from mqtt import mqtt_publisher
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *


@receiver(post_save, sender=LiveEvent)
def create_live_event(sender, instance, **kwargs):
	DOMAIN_NAME = config.DOMAIN_NAME
	json_msg ={
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "LiveEvent",
		"name": instance.name,
		"user": instance.user.id,
		"audio": f"{DOMAIN_NAME}/{instance.audio.url}",
		"audio_duration": instance.audio_duration,
		"created_at":instance.created_at
	}}
	#print(instance.user.topic)
	self_topic = instance.user.topic.serial_number
	# ensure_ascii for decode arabic characters
	json_msg_publisher = json.dumps(json_msg, ensure_ascii=False,default=str)
	mqtt_publisher.main(topic=f"raspberry_pi/{self_topic}", message=json_msg_publisher)


@receiver(post_save, sender=PrayerEvent)
def create_after_before_event(sender, instance, **kwargs):
	DOMAIN_NAME = config.DOMAIN_NAME
	json_msg = {
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "PrayerEvent",
		"type": instance.type,
		"name": instance.name,
		"user": instance.user.id,
		"prayer": instance.prayer,
		"audio": f"{DOMAIN_NAME}/{instance.audio.url}",
		"audio_duration": instance.audio_duration,
		"created_at":instance.created_at
	}}
	# print(instance.user.topic)

	# ensure_ascii for decode arabic characters
	json_msg_publisher = json.dumps(json_msg, ensure_ascii=False,default=str)
	mqtt_publisher.main(topic=f'raspberry_pi/{instance.user.topic.serial_number}',
						message=json_msg_publisher)


@receiver(post_save, sender=PrayerAudio)
def create_prayer_audio(sender, instance, **kwargs):
	DOMAIN_NAME = config.DOMAIN_NAME
	json_msg ={
	"operation": "transfer",
	"sender": 0,
	"data": {
		"model": "PrayerAudio",
		"prayer": instance.prayer,
		"user": instance.user.id,
		"audio": f"{DOMAIN_NAME}/{instance.audio.url}",
		"audio_duration": instance.audio_duration
	}}
	# ensure_ascii for decode arabic characters
	json_msg_publisher = json.dumps(json_msg, ensure_ascii=False,default=str)
	mqtt_publisher.main(topic=f"raspberry_pi/{instance.user.topic.serial_number}",
						message=json_msg_publisher)


@receiver(post_save, sender=State)
def send_offset_time_to_clients(sender, instance, **kwargs):
	"""
	* this signal for forward offset_time to all instance state topics
	"""
	mosques = Mosque.objects.filter(state=instance)
	for mosque in mosques:
		current_topic = mosque.topic
		json_msg={
		"operation": "transfer",
		"sender": 0,
		"data": {
		"model": "constance",
		"offset_time": current_topic.state.offset_time
		}} 
		json_msg_publisher=json.dumps(json_msg,ensure_ascii=False)  #ensure_ascii for decode arabic characters
		mqtt_publisher.main(topic=f"raspberry_pi/{current_topic.serial_number}", message=json_msg_publisher)


@receiver(post_save, sender=Mosque)
def send_offset_time_to_client(sender, instance, **kwargs):
	"""
	* this signal for forward offset_time to self mosque topic
	"""
	json_msg={
		"operation": "transfer",
		"sender": 0,
		"data": {
		"model": "constance",
		"offset_time": instance.state.offset_time
		}} 
	json_msg_publisher=json.dumps(json_msg,ensure_ascii=False)  #ensure_ascii for decode arabic characters
	mqtt_publisher.main(topic=f"raspberry_pi/{instance.topic.serial_number}", message=json_msg_publisher)
