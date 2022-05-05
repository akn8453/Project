import paho.mqtt.publish as publish
import json
from datetime import datetime
from time import sleep
import string

think_channelID= "1664615"
api_write_key = "599OB0IMDX0LJUHA"

t_transport = "websockets"
t_port = 80

mqtt_host = "mqtt.thingspeak.com"
mqtt_username = "Bj0kCBQ4DDQ6Ix4VHCQ1Cxk"
mqtt_client_ID = "Bj0kCBQ4DDQ6Ix4VHCQ1Cxk"
mqtt_password = "W7x/VeBRK/Rxz7FF5lHQqJQ1"


payload = "field3=" + str(1)



topic = "channels/" + think_channelID + "/publish/"+api_write_key

print ("Writing Payload = ", payload," to host: ", mqtt_host, " clientID= ", mqtt_client_ID, " User ", mqtt_username, " PWD ", mqtt_password)
publish.single(topic, payload, hostname=mqtt_host, transport=t_transport, port=t_port, client_id=mqtt_client_ID, auth={'username':mqtt_username,'password':mqtt_password})

