# subscriber
import paho.mqtt.client as mqtt

#====================================================
# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic_Humidity = "TEALE/Humidity"
MQTT_Topic_Temperature = "TEALE/Temperature"
#====================================================

mqttc = mqtt.Client()
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

def on_connect(client, userdata, flags, rc):
    print("Connected to a broker!")
    mqttc.subscribe(MQTT_Topic_Humidity)

def on_message(client, userdata, message):
    print(message.payload.decode())

while True:
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.loop_forever()