import pyshark
import time,sys
import csv,configparser
from datetime import datetime
mqttclient={}
mykey=""
max_declined=0
timebound_limit=30
disconnection_count=4
disconnection_groupcount=4
network_interface=""


parser=configparser.ConfigParser()
parser.read('bruteconfig')
for sect in parser.sections():
   print('Section:', sect)
   for k,v in parser.items(sect):
      print(' {} = {}'.format(k,v))
      if k=='timelimit':
         timebound_limit=int(v)
      elif k=='count':
         disconnection_count=int(v)
      elif k=='groupcount':
         disconnection_groupcount=int(v)
   print()
   
parser.read('../config1')
for sect in parser.sections():
   print('Section:', sect)
   for k,v in parser.items(sect):
      print(' {} = {}'.format(k,v))
      if k=='interface':
         network_interface=str(v)
   print()

#print(f'{timebound_limit} {disconnection_count} {disconnection_groupcount}')

def timebound(key):
    global mqttclient
#check if difference is greater than 10 sec from start of analysis
    if(((mqttclient[key]['count_time']) - (mqttclient[key]['start_time'])) >= timebound_limit):
        print(f"timeout [{key}].....{(mqttclient[key]['count_time']) - (mqttclient[key]['start_time'])}")
        mqttclient[key]['start_time']=time.time()
        
        return 0
    else:
        return 1


def grouptimebound():
    print('---------------------')
    global starttime,max_declined,timebound_limit
    #print(f"{time.time()-starttime} > {timebound_limit+10}")
    if (time.time()-starttime) > timebound_limit+10:
       print("Global Timeout.....")
       max_declined=0
       starttime=time.time()
       return 0
    else:
       return 1      

def printresponsecode(pkt):

    global mqttclient,mykey,max_declined,counttime
    #if packet is mqtt packet
    if 'mqtt' in dir(pkt):

        #store p address of client requesting connection
        attackip=pkt.ip.dst
        mykey=str(attackip)
        victimip=str(pkt.ip.src)
        #print(f"msgtype:{pkt.mqtt.msgtype}")

        #if message type is connct ack
        if int(pkt.mqtt.msgtype) == 2:
            #print response code
                print(f"response code: {pkt.mqtt.conack_val} ")#{pkt.mqtt.conack.val}
                #if response code is 4 or 5 add or update entry
                if(int(pkt.mqtt.conack_val) == 0):
                    if str(attackip) in mqttclient.keys():
                        if mqttclient[mykey]['count'] > disconnection_count:
                            print(f"Intrusion successful by ip {mykey}")
                            row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'Intruded',victimip,mykey,mqttclient[mykey]['count']]
                            with open("../GUI/node/webGUI/mycsv.csv","a") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)
                if((int(pkt.mqtt.conack_val) == 5) or (int(pkt.mqtt.conack_val) == 4)):
                    max_declined+=1
                    #print(f"countgroup={max_declined}")
                    #if ip already exist inncrease count by 1 else add entry for that IP
                    if str(attackip) in mqttclient.keys():
                        mqttclient[mykey]['count']=(mqttclient[mykey]['count']) + 1
                        mqttclient[mykey]['count_time']=time.time()
                        print(f"{mqttclient}")
                        #if any IP has reqested to connect with wrong creditionals more than 4 time within 10 sec then attck is happning
                        if mqttclient[mykey]['count']>disconnection_count and timebound(mykey):
                            print(f"Blacklist ip {mykey}")
                            row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'BruteForce',victimip,mykey,mqttclient[mykey]['count']]
                            with open("../GUI/node/webGUI/mycsv.csv","a") as f:
                                writer = csv.writer(f)
                                writer.writerow(row)

                        if grouptimebound() and max_declined >disconnection_groupcount :
                            flag=0
                            for ip in mqttclient.keys():
                                if mqttclient[mykey]['count']>disconnection_count:
                                    row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'BruteForce',victimip,str(ip),mqttclient[str(ip)]['count']]
                                else:
                                    flag=1
                                    row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'GroupBruteForce',victimip,str(ip),mqttclient[str(ip)]['count']]
                                with open("../GUI/node/webGUI/mycsv.csv","a") as f:
                                    writer = csv.writer(f)
                                    writer.writerow(row)
                            if flag==1:
                                print(f"Group bruteforce possible....{max_declined}")
                                flag=0
                            


                    else:
                        mqttclient[mykey]={'count':1,'count_time':time.time(),'start_time':time.time()}
                        #print(f"else ip {attackip} \n {mqttclient}")



starttime=time.time()
counttime=time.time()

capture = pyshark.LiveCapture(interface="wlan0",bpf_filter='tcp port 1883', output_file='mysamplepcap.pcap')


capture.apply_on_packets(printresponsecode)



