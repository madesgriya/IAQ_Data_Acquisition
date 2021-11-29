#neflix testing

import json, random, threading
import paho.mqtt.client as mqtt
from datetime import datetime

mqttc = mqtt.Client()
MQTT_broker = "mqtt.intuitive.works"
MQTT_port = 1883
Keep_Alive_Interval = 45
topic = "netflix/f8:f0:05:e8:c5:98"
user = "Teale"
password = "TRuhC3jBFr3b"

mqttc.connect(MQTT_broker,int(MQTT_port),int(Keep_Alive_Interval))
mqttc.username_pw_set(user, password=password) 

def on_connect(client, userdata, flags, rc):
    mqttc.subscribe(topic, 0)

def on_message(mosq, obj, msg):
    msg_dec = msg.payload.decode("utf-8")
    msg_clear = json.loads(msg_dec)
    json_file = {}
    json_file["Name"] = msg_clear[0]["Name"]
    json_file["Sensor_id"] = msg_clear[0]["Sensor_id"]
    json_file["State"] = msg_clear[0]["State"] 
    myDate = msg_clear[0]["timestamp"]
    json_file["timestamp"] = datetime.fromtimestamp(int(myDate)/1000).strftime("%Y-%m-%d %H:%M:%S")
    occupancy = json.dumps(json_file)
    print(occupancy)

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def on_subscribe(mosq, obj, mid, granted_qos):
    pass

while True:
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log
    mqttc.loop_forever()
    mqttc.disconnect()
