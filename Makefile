init:
	#cd ~
	#curl -sL https://deb.nodesource.com/setup_16.x | sudo bash -
	#cat /etc/apt/sources.list.d/nodesource.list
	#deb https://deb.nodesource.com/node_16.x focal main
	#deb-src https://deb.nodesource.com/node_16.x focal main
	cat requirement.txt | xargs apt install -y
	$(info ------------ubuntu requirements completed--------------)
	pip3 install -r pyrequirement.txt
	$(info ------------python requirements completed--------------)
	cat npmrequirement.txt | xargs npm install -y
	$(info ------------ubuntu requirements completed--------------)
	
mosquitto_configure:
	sudo cp myconfig.conf /etc/mosquitto/conf.d
	cd /etc/mosquitto/
	mosquitto_passwd -c mypass.txt cdacuser
	set pass "cdacpass" 
	expect "password: "
	send "$pass"
	expect "password: "
	send "$pass"
	

autostart:	
	cp technetServerStart.service /lib/systemd/system
	systemctl daemon-reload
	systemctl enable technetServerStart.service
	$(info -----technnetServer autostart on boot setup completed---)
	
disable_autostart:
	systemctl disable technetServerStart.service
	$(info -----technnetServer autostart on boot setup disabled---)

stop:
	sudo systemctl stop technetServerStart.service
	
start:
	sudo systemctl start technetServerStart.service	
	

mongodb:
	curl -fsSL https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
	apt-key list
	echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
	apt update
	apt install -y mongodb-org
	$(info ----------mongodb-org installation completed-----------)
	systemctl start mongod.service
	systemctl status mongod
	systemctl service mongod start
