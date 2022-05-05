import paho.mqtt.client as mqtt
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime

#---------initializing mongoDB connection parameters---------------------------------------------------
client = MongoClient('mongodb://localhost:27017/')
db = client.technet
tempcollection =db.temperature
humcollection  =db.humidity
ledcollection  =db.LED

#-----------onconnecting to mosquitto broker----------------------------------------------------
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe("room1/temp")  # Subscribe to the topic “room1/temp”, receive any messages published on it
    client.subscribe("room1/hum")
    client.subscribe("room1/LED")
#-----------on recieving message on topic
def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    #print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    
    #create json file having timestamp,topic,val--------------------------------------------------------
    data = {}
    data["timestamp"] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    data["topic"]=str(msg.topic)
    data["val"]=float(msg.payload)
    json_data_str=json.dumps(data)
    print(json_data_str)
    if str(msg.topic) == "room1/temp":
    	tempcollection.insert_one(data)
    elif str(msg.topic) == "room1/hum":
    	humcollection.insert_one(data)
    elif str(msg.topic) == "room1/LED":
    	ledcollection.update_one({"topic":"room1/LED"}, {"$set": { "val": float(msg.payload), "timestamp": (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f") }},upsert=True)
     	#ledcollection.insert_one(data)
    


client = mqtt.Client("mongologger")  # Create instance of client with client ID “mongologger”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect('192.168.1.100', 1883)
client.loop_forever()  # Start networking daemon
#client.close
