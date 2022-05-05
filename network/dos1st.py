import pyshark
import time,sys
import csv,configparser
from datetime import datetime
maxNumberOfClients = 3
time_window = 3
packet_len = 23
network_interface=""

packetcount=0
totallength=0
starttime=time.time()
attackip=""
victimip=""

def length(pkt,currtime):
    global starttime,totallength,time_window
    totallength+=int(pkt.tcp.len)
    if currtime-starttime > time_window:
    	return totallength
    else:
    	return 0

def timelimit(currtime):
   global starttime,time_window,packetcount,totallength
   if currtime-starttime > time_window:
   	starttime=time.time()
   	return 1
   else:
   	return 0

def packet_callback(pkt):
    currtime=time.time()	
    global packetcount,starttime,totallength,attackip,victimip
    if 'mqtt' in dir(pkt) and int(pkt.mqtt.msgtype) == 3:
        attackip=str(pkt.ip.src)
        victimip=str(pkt.ip.dst)
        packetcount+=1
        length(pkt,currtime)
    	
    if timelimit(currtime):   
    	if totallength>packet_len*maxNumberOfClients*2:
    	    print(f"within {time_window} total length is {totallength}")
    	    row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'dos_totaldatasize',victimip,attackip,totallength]
    	    with open("../GUI/node/webGUI/mycsv.csv","a") as f:
    	        writer = csv.writer(f)
    	        writer.writerow(row)
    	if packetcount>maxNumberOfClients*2:
    	    print(f"logging  packet count {packetcount}")
    	    row=[(datetime.today()).strftime("%d-%b-%Y %H:%M:%S"),'dos_published_messages',victimip,attackip,packetcount]
    	    with open("../GUI/node/webGUI/mycsv.csv","a") as f:
    	        writer = csv.writer(f)
    	        writer.writerow(row)   
    	totallength=0
    	packetcount=0
    	pass
#    else packetcount>maxNumberOfClients*2:
#        print(f"publish messages excceded {packetcount} > {maxNumberOfClients*2}")
            

parser=configparser.ConfigParser()
parser.read('dosconfig')
for sect in parser.sections():
   print('Section:', sect)
   for k,v in parser.items(sect):
      print(' {} = {}'.format(k,v))
      if k=='maxclients':
         maxNumberOfClients=int(v)
      elif k=='time':
         time_window=int(v)
      elif k=='len':
         packet_len=int(v)
   print()
   
parser.read('../config1')
for sect in parser.sections():
   print('Section:', sect)
   for k,v in parser.items(sect):
      print(' {} = {}'.format(k,v))
      if k=='interface':
         network_interface=str(v)
   print()

print(f'{maxNumberOfClients} {time_window} {packet_len} {network_interface}')





capture = pyshark.LiveCapture(interface="wlan0",bpf_filter='tcp port 1883', output_file='mysamplepcap.pcap')
capture.apply_on_packets(packet_callback)






