import sys
import paho.mqtt.client as mqtt
import json
from datetime import datetime
from django.conf import settings
from constance import config

from adan.models import Topic,Mosque,State
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected with result code : 0")
    client.subscribe("raspberry_pi/#", qos=1)
def get_mosque_status(topic)->bool:
    """
    get raspbery pi topic status on realtime
    """
    import requests
    from constance import config
    BASE_URL = config.BASE_MQTT_API_URL
    username = config.MQTT_USERNAME
    password = config.MQTT_PASSWORD
    response = requests.get(
        f'{BASE_URL}/clients/{topic.serial_number}', auth=(username, password))
    response_dict = json.loads(response.text)
    try:
        if response_dict['connected']:
            return True
        else:
            return False
    except:
        return False
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        brut_text = str(msg.payload.decode("utf-8"))
        json_msg = json.loads(brut_text)
        if json_msg["sender"] == 1:
            if json_msg["operation"] == "init":
                if json_msg["data"]["model"] == "Topic":
                    # Get the the mosque name 
                    mosque_name=json_msg["data"]["mosque_name"]
                    # Get the serial number from the topic
                    topic_serial_number = json_msg['data']['topic_serial_number']
                    #** check if topic is exist 
                    if Topic.objects.filter(serial_number=topic_serial_number).exists():
                        topic=Topic.objects.get(serial_number=topic_serial_number)
                    else:
                        topic=Topic(serial_number=topic_serial_number,name=mosque_name)
                        topic.save()
                    if not Mosque.objects.filter(topic=topic).exists():
                        Mosque.objects.create(topic=topic,name=mosque_name)
                    mosque_status=get_mosque_status(topic=topic) # get raspberryPi status
                    Mosque.objects.filter(topic=topic).update(status=mosque_status) # modefy raspberryPi status
            elif json_msg ["operation"]=="transfer":
                if json_msg["data"]["model"]=="Plug":
                    speaker_status=json_msg["data"]["state"]
                    serial_number=json_msg["data"]["topic_serial_number"]
                    try:topic = Topic.objects.get(serial_number=serial_number)
                    except:topic=None
                    if topic:
                        status = False if speaker_status =="off" else True
                        Mosque.objects.filter(topic=topic).update(speaker_status=status)
            #** create topic & mosque 
            # Get the topic
    except Exception as e:
        print(e)

def main():
    client = mqtt.Client(client_id="API", clean_session=False)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect_async(config.broker_ip, 1883, 60)
    return client
if __name__ == '__main__':
	main()
	sys.exit(0)
