#!/usr/bin/env python3
import os
if __name__ == '__main__':
    os.system("mosquitto -c /etc/mosquitto/conf.d/myconfig.conf -d")
    print("mosquitto -c /etc/mosquitto/conf.d/myconfig.conf -d")
    os.system("python3 -u /home/ubuntu/technet/mongo/mqttLogToAtlas.py &")
    print("python3 -u /home/ubuntu/technet/mongo/mqttLogToAtlas.py &")
    os.system("node /home/ubuntu/technet/GUI/node/webGUI/finalservermongo.js")
    print("node /home/ubuntu/technet/GUI/node/webGUI/finalservermongo.js")
    #os.system("touch /home/$USER/technet/newautostart.txt")
    #os.system("mongod")
    #os.system("mongo --eval 'db.runCommand({ connectionStatus: 1 })'")
