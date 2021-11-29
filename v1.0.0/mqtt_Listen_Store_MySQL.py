import json
import sys
import mariadb
import paho.mqtt.client as mqtt
import ssl
import pymysql

########RDS INSTANCE VIA BASTION SERVER#######
#mariadb_connection = pymysql.connect(
#  host = 'sp02ubnmariadb.c0x2xygsiwvl.ap-southeast-1.rds.amazonaws.com',
#  user = 'su',
#  password = 'tealesg1',
#  port = 3306,
#  db = 'iotdb',
#  cursorclass = pymysql.cursors.DictCursor
#)
##############################################

mariadb_connection = pymysql.connect(
  host = 'hostname IP', 
  user = 'username',
  password = 'password',
  port = 3307,
  db = 'db_name',
  cursorclass = pymysql.cursors.DictCursor
)
cursor = mariadb_connection.cursor()

#cursor.execute("create database dummy;")

# MQTT Settings 
MQTT_Broker = "test.mosquitto.org"
MQTT_Port = 1883
Keep_Alive_Interval = 60
MQTT_Topic = "TEALE/Pagoda33b/Temperature"
mqttc = mqtt.Client()

# Connect
### mqttc.tls_set(ca_certs="ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
#mqttc.username_pw_set(user, password=password) 

# Subscribe
def on_connect(client, userdata, flags, rc):
  mqttc.subscribe(MQTT_Topic, 0)

def on_message(mosq, obj, msg):
  msg_dec = msg.payload.decode('utf-8')#translate(None, '{}""').split(", ")
  msg_clear = json.loads(msg_dec)
  
  ###################################
  #nodeName = msg_clear['nodeName']
  #reportTime = msg_clear['reportTime']
  #meterValue = msg_clear['meterValue']
  #neterUnit = msg_clear['meterUnit']
  
  # msg_dict = {} #not needed as the messages are received in JSON format
  #for i in range(0, len(msg_clear)):
  #      msg_dict[msg_clear[i].split(": ")[0]] = msg_clear[i].split(": ")[1]
  ######################################
  
  # Prepare dynamic sql-statement
  #placeholders = ','.join(['%s'] * len(msg_clear)) 
  placeholders = ','.join(str(v) for v in msg_clear.values())
  columns = ', '.join(msg_clear.keys())

  #sql = "INSERT INTO temperature (%s) VALUES (%s)" % (columns, placeholders)
  sql = "INSERT INTO temperature (%s,%s,%f,%f) VALUES (%f,%f,%f,%f)" % (columns, placeholders)
  # Save Data into DB Table
  try:
      cursor.execute(sql, msg_clear.values())
  except mariadb.Error as error:
      print("Error: {}".format(error))
  mariadb_connection.commit()
  print(cursor.rowcount, 'Data saved!')

def on_subscribe(mosq, obj, mid, granted_qos):
  pass

# Assign event callbacks
while True:
      mqttc.on_message = on_message
      mqttc.on_connect = on_connect
      mqttc.on_subscribe = on_subscribe
      #Continue the network loop 
      mqttc.loop_forever()
      # #close db-connection
      mariadb_connection.close()
