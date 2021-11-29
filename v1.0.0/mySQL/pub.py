# publisher
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

###################Manual Publishing#####################
client = mqtt.Client()
client.connect('test.mosquitto.org', 1883)

while True:
    client.publish("TEALE/test", input('Message : '))