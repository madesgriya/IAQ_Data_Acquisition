# publisher
import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime

###################Manual Publishing#####################
#client = mqtt.Client()
#client.connect('test.mosquitto.org', 1883)

#while True:
#    client.publish("TEALE/Humidity", input('Message : '))

#====================================================
# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic_Humidity = "TEALE/Pagoda33b/Humidity"
MQTT_Topic_Temperature = "TEALE/Pagoda33b/Temperature"
#====================================================

def on_connect(client, userdata, rc):
        if rc != 0:
                pass
                print("Unable to connect to MQTT Broker...")
        else:
                print("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
        pass

def on_disconnect(client, userdata, rc):
        if rc !=0:
                pass

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))


def publish_To_Topic(topic, message):
        mqttc.publish(topic,message)
        print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print("")


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

def publish_Fake_Sensor_Values_to_MQTT():
        threading.Timer(3.0, publish_Fake_Sensor_Values_to_MQTT).start()
        global toggle
        if toggle == 0:
                Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(50, 100)))
                Humidity_Data = {}
                Humidity_Data['nodeName'] = "humidity_dummy"
                Humidity_Data['reportTime'] = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
                Humidity_Data['meterValue'] = Humidity_Fake_Value
                Humidity_Data['meterUnit'] = "%"
                Humidity_json_data = json.dumps(Humidity_Data, indent=4, sort_keys=False)

                print("Publishing fake Humidity Value: " + str(Humidity_Fake_Value) + "...")
                publish_To_Topic (MQTT_Topic_Humidity, Humidity_json_data)
                toggle = 1
        
        else:
                Temperature_Fake_Value = float("{0:.2f}".format(random.uniform(15, 30)))
                Temperature_Data = {}
                Temperature_Data['nodeName'] = "temperature_dummy"
                Temperature_Data['reportTime'] = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
                Temperature_Data['meterValue'] = Temperature_Fake_Value
                Temperature_Data['meterUnit'] = "°C"
                temperature_json_data = json.dumps(Temperature_Data, indent=4, sort_keys=False)

                print("Publishing fake Temperature Value: " + str(Temperature_Fake_Value) + " ...")
                publish_To_Topic(MQTT_Topic_Temperature, temperature_json_data)
                toggle = 0

publish_Fake_Sensor_Values_to_MQTT()