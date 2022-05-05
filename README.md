# Project TechNet(2021-22)


### Install Dependencies:
-Run this command to install all dependencies at a time
	```
	sudo make init
	```

- **Ubuntu Dependency:**
  - Run following command
	```
	cat requirement.txt | xargs apt install -y
	```
  - To use wireshark as non root user
  	```
   	sudo dpkg-reconfigure wireshark-common
   	sudo chmod +x /usr/bin/dumpcap
   	```
- **Python Dependency:**
  - Run following command
	```
	pip3 install -r pyrequirement.txt
	```
- **Node Dependency:**
  - Run following command
	```
	cat npmrequirement.txt | xargs npm install -y
	```
  - NodeJs version should be 16.x+. If not install it by including repo mentioned below
	```
	cd ~
	curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
	sudo apt-get install nodejs
	```
  - To initialise all npm packages naviagate to GUI/node folder 
	```
	cd GUI/node
	npm init
	npm i
	```
### Autostart server script:
- run following command in technet folder to do all configuration for autostart
	```
	sudo make autostart
	```
- **Disable Autostart at boot:**
  - Run following command
	```
	make disable_autostart
	```
- **Manual stop server:**
  - Run following command
	```
	make stop
	```
- **Manual start server:**
  - Run following command
	```
	make start
	```
### mosquitto configuration:
- run following command to set username and password for mosuqitto broker
	```
	sudo make mosquitto_configure
	```
### Install mongoDB:
- run following command in technet folder to install mongodb on local machine
	```
	sudo make mongodb
	```
### Configuration files:
- mosquitto borker and mongo ```technet/config1```
- dos ```technet/network/dosconfig``` 
- BruteForce ```technet/network/bruteconfig```

### Attack detection:
- run following command in technet folder to run attack detection algorithms
	```
	cd network
	sudo python3 Bruteforcefinal.py &
	sudo python3 dosfinal.py &
	```
this will log attack details in CSV file also will be visible on web based GUI as pie chart as well as table
go to ```<ip>:1234/```
