import paho.mqtt.client as mqtt
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime

#mongourl="mongodb+srv://technet:awesomeproject@technetmongo.kalqd.mongodb.net/technetmongo?retryWrites=true&w=majority"
mongourl=""
mqtt_broker=""
mqtt_port=1883
mqtt_user=""
mqtt_password=""

import configparser
parser=configparser.ConfigParser()
parser.read('/home/ubuntu/technet/config1')

for sect in parser.sections():
    print('Section:', sect)
    for k,v in parser.items(sect):
        print(' {} = {}'.format(k,v))
        if k=='mongodb_url':
            mongourl=str(v)
        elif k=='mosquitto_ip':
            mqtt_broker=str(v)
        elif k=='mosquitto_port':
            mqtt_port=int(v)
        elif k=='mosquitto_username':
            mqtt_user=str(v)
        elif k=='mosquitto_password':
            mqtt_password=str(v)
    print()

print(f"{mongourl} {mqtt_broker} {mqtt_port} {mqtt_user} {mqtt_password}")


#---------initializing mongoDB connection parameters---------------------------------------------------
client = MongoClient(mongourl)
db = client.technet
temp1collection =db.temperature1
temp2collection =db.temperature2
humcollection  =db.humidity
ledcollection  =db.LED

#-----------onconnecting to mosquitto broker----------------------------------------------------
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("room1/temp")  # Subscribe to the topic “room1/temp”, receive any messages published on it
    client.subscribe("room2/temp")  
    client.subscribe("room1/hum")
    client.subscribe("room1/LED")
#-----------on recieving message on topic
def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    #print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    
    #create json file having timestamp,topic,val--------------------------------------------------------
    data = {}
    data["timestamp"] = (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")
    data["topic"]=str(msg.topic)
    data["val"]=float(msg.payload)
    json_data_str=json.dumps(data)
    print(json_data_str)
    if str(msg.topic) == "room1/temp":
    	temp1collection.insert_one(data)
    elif str(msg.topic) == "room2/temp":
    	temp2collection.insert_one(data)
    elif str(msg.topic) == "room1/hum":
    	humcollection.insert_one(data)
    elif str(msg.topic) == "room1/LED":
    	ledcollection.update_one({"topic":"room1/LED"}, {"$set": { "val": float(msg.payload), "timestamp": (datetime.today()).strftime("%Y-%m-%d %H:%M:%S")  }},upsert=True)
     	#ledcollection.insert_one(data)
    


client = mqtt.Client("mongologger")  # Create instance of client with client ID “mongologger”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
client.username_pw_set(mqtt_user,mqtt_password)
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect(mqtt_broker, mqtt_port)
client.loop_forever()  # Start networking daemon
client.close
