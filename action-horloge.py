#!/usr/bin/env python3
from datetime import datetime
from pytz import timezone
import paho.mqtt.client as paho
import json

MQTT_IP_ADDR = "localhost"
MQTT_PORT = 1883
MQTT_ADDR = "{}:{}".format(MQTT_IP_ADDR, str(MQTT_PORT))

def verbalise_hour(i):
	if i == 0:
		return "minuit "
	elif i == 1:
		return "une heure "
	elif i == 12:
		return "midi "
	elif i == 21:
		return "vingt et une heures "
	else:
		return "{0} heures ".format(str(i)) 

def verbalise_minute(i):
	if i == 0:
		return ""
	elif i == 1:
		return "une"
	elif i == 21:
		return "vingt et une"
	elif i == 31:
		return "trente et une"
	elif i == 41:
		return "quarante et une"
	elif i == 51:
		return "cinquante et une"
	else:
		return "{0}".format(str(i)) 

def on_connect(client, userdata, flags, rc):
    print("Connected to {0} with result code {1}".format(MQTT_IP_ADDR, rc))
    client.subscribe('hermes/intent/cedcox:askTime')

def on_message(client, userdata, msg):
    print("Message received on topic {0}: {1}"\
        .format(msg.topic, msg.payload))
    
    payload = json.loads(msg.payload)
    name = payload["intent"]["intentName"]
    slots = payload["slots"]
    sessionId = payload["sessionId"]

    print("Intent {0} detected with slots {1} and seesionId {2}"\
        .format(name, slots, sessionId))
    
    sentence = 'Il est '

    now = datetime.now(timezone('Europe/Paris'))

    sentence += verbalise_hour(now.hour) + verbalise_minute(now.minute)
    print(sentence)

    monjson=json.dumps({"sessionId": sessionId,"text": sentence})
    client.publish("hermes/dialogueManager/endSession",monjson)#publish


client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_IP_ADDR, MQTT_PORT, 60)
client.loop_forever()
