import sys
import paho.mqtt.client as mqtt
from .models import *
import json
from datetime import datetime
# The callback for when the client receives a CONNACK response from the server.

def on_connect(client, userdata, flags, rc):
    print("\n",datetime.now(), "  ", "Connected with result code "+str(rc) + "\n")

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("raspberry_pi/#", qos=1)

def main(topic, message):
    client = mqtt.Client(client_id='1', clean_session=False)
    client.on_connect = on_connect
    client.connect("142.44.163.144", 1883, 60)
    client.publish(topic, message, qos=1)

if __name__ == '__main__':
	main()
	sys.exit(0)
