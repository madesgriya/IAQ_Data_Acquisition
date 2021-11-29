import json
import sys
import ssl
import logging
import asyncio
import paho.mqtt.client as mqtt
import pymysql

logger = logging.getLogger(__name__)

#====================================================
# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic_Humidity = "TEALE/test" #----->to be edited
MQTT_Topic_Temperature = "TEALE/Temperature"
#====================================================

mqttc = mqtt.Client()
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

def on_connect(client, username, falgs, rc):
    print("connected with result code" + str(rc))
    mqttc.subcribe(MQTT_Topic_Humidity, 0)

def on_message(mosq, obj, msg):
    """
    run this query in mysql:
    ////////////////////
    create database dummies;
    use dummies;
    CREATE TABLE mqttpy (
    id int auto_increment not null,
    messages varchar(255) not null,
    time timestamp default current_timestamp,
    primary key (id)
    );
    //////////////////  
    """
    print(msg.payload.decode())

    yield from mqttc.connect('mqtt://test.mosquitto.org:1883/')
    yield from mqttc.subscribe([
        ("TEALE/test", QOS_1)
    ])
    logger.info('Subscribed!')
    try: 
        for i in range(1,100):
            message = yield from C.deliver_message()
            packet = message.publish_packet
            print(packet.payload.data.decode('utf-8'))
            con = pymysql.connect(
                host = 'localhost',
                user = 'root',
                password = 'Zxptitak01.',
                port=3306,
                db = 'mqttpy',
                cursorclass = pymysql.cursors.DictCursor
            )
            cursor = con.cursor()
            sql = '''insert into mqttpy (messages) values (%s)'''
            val = str(packet.payload.data.decode('utf-8'))
            cursor.execute(sql, val)
            con.commit()
            print(cursor.rowcount, 'Data saved!')
    except MySQLdb.Error as error:
        print("Error: {}".format(error))
    
def on_subscribe(mosq, obj, mid, granted_qos):
    pass

while True:
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.loop_forever()
