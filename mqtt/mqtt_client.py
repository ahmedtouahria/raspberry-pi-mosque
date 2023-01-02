import paho.mqtt.client as mqtt
import json
from datetime import datetime
from django.conf import settings
from constance import config

# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected with result code : 0")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("raspberry_pi/#", qos=1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        brut_text = str(msg.payload.decode("utf-8"))
        json_msg = json.loads(brut_text)
        if json_msg["sender"] == 1:
            # if json_msg["operation"] == "transfer":
            #     if json_msg["data"]["model"] == "PrayerAudio":
            #         pass
            # Get the serial number from the topic
            print(str(msg.topic).replace("raspberry_pi/", ""))
            # Get the topic
            print(str(msg.topic))
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
