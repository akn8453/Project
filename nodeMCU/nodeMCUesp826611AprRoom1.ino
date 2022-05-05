

/****************************WIFIneeds**************************************************/
#include <ESP8266WiFi.h>
String mySSID[] = {"projectTechNet", "godspeed"};
String myPASSWORD[] = { "itsmyproject", "connectit"};
/****************************other library*************************/
#include<SoftwareSerial.h>
#include<PubSubClient.h>

#include <math.h>
#define LEDPIN D1 //
#define TEMPPIN A0
double Thermister(int RawADC) {
  if (RawADC == 0) {
    return 0;
  }
  double Temp;
  Temp = log(((10240000 / RawADC) - 10000));
  Temp = 1 / (0.001129148 + (0.000234125 + (0.0000000876741 * Temp * Temp )) * Temp ); Temp = Temp - 273.15; // Convert Kelvin to Celcius
  return Temp;
}

/***************************declarations*********************************/
//Wifi declaration
int wififlag = 0;
double temp = 0;
String SSID1 = "", PASSWORD1 = "", data = "";
char * mqtt_data;
//MQTT Declaration
const char* mqtt_server = "192.168.1.100";
const int mqtt_port = 1883;
const char* mqtt_username = "cdacuser";
const char* mqtt_password = "cdacpass";
const char* mqtt_topic_temp = "room1/temp";
const char* mqtt_topic_hum = "room1/hum";
const char* mqtt_clientID = "ESP8266_DHT22";


void callback(char* topic, byte* payload, unsigned int length1) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message: ");
  String message = "";
  for (int i = 0; i < length1; i++) {
    Serial.print((char)payload[i]);
    message += (char)payload[i];
  }
  Serial.println();
  Serial.println("______________________________________");

  if (String(topic) == "room1/LED") {
    if (message == (String)1) {
      digitalWrite(LEDPIN, HIGH);
    }
    else if (message == (String)0) {
      digitalWrite(LEDPIN, LOW);
    }

  }


}

// Initialise the WiFi and MQTT Client objects
WiFiClient wifiClient;
PubSubClient client(mqtt_server, mqtt_port, callback, wifiClient); // 1883 is the listener port for the Broker

void mywifi()
{
  int i = 0;
  const char* my_SSID = SSID1.c_str();
  const char* my_PASSWORD = PASSWORD1.c_str();
  WiFi.begin(my_SSID, my_PASSWORD);
  int wificount = 0;                          //for providing time slot for connection establishment
  Serial.println("");
  Serial.print("CONNECTING to :- ");
  Serial.println(my_SSID);
  while (WiFi.status() != WL_CONNECTED)       //till wifi gets  connected
  {
    delay(1000);
    wificount++;
    Serial.print(" " + (String)wificount);
    wififlag = 1;
    if (wificount == 15)                      // if does not get coonected in 15 seconds
    {
      i++;                                    //use second elements in ssid and password array
      wififlag = 0;                           //make flag zero to represent that not got connected
      break;
    }
  }
  if (wififlag)                               //if flag is one that means got connected and so print name of wifi
  {
    Serial.println(" ");
    Serial.print("conected to ");
    Serial.print(my_SSID);
    Serial.println(WiFi.localIP());
    i = 0;
  }
  else                                        //if flag is zero that means need to try for next ssid and password
  {
    SSID1 = mySSID[i];
    PASSWORD1 = myPASSWORD[i];
    return mywifi();                          //attempt again
  }
}
/*******************************ARDUINO SETUP*****************************************/
void setup()
{
  Serial.begin(115200);
  SSID1 = mySSID[0];
  PASSWORD1 = myPASSWORD[0];
  pinMode(LEDPIN, OUTPUT);
  digitalWrite(LEDPIN, LOW);
  mywifi();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  // Connect to MQTT Broker
  // client.connect returns a boolean value to let us know if the connection was successful.
  if (client.connect(mqtt_clientID)) {
    Serial.println("Connected to MQTT Broker!");
    client.subscribe("room1/LED");
  }
  else {
    Serial.println("Connection to MQTT Broker failed...");
  }

}
void loop()
{
  client.loop();//for subscribe
  delay(1000);
  /**************************************************/
  if (WiFi.status() != WL_CONNECTED)          //check for wifi is connectiom if not connected then attempt with all listed connection
  {
    SSID1 = mySSID[0];
    PASSWORD1 = myPASSWORD[0];
    mywifi();
  }
  /**************************************************/
  temp = Thermister(analogRead(TEMPPIN));
  data = (String)temp;
  // PUBLISH to the MQTT Broker (topic = room1/temprature)
//  Serial.print(temp);  // display Fahrenheit
//      Serial.println("f");
  if (temp != 0) {
    if (client.publish(mqtt_topic_temp, (char*)data.c_str())) {
      Serial.print("message sent- temprature:");
      Serial.print(temp);  // display Fahrenheit
      Serial.println("c");
    }
    // Again, client.publish will return a boolean value depending on whether it succeded or not.
    // If the message failed to send, we will try again, as the connection may have broken.
    else {
      Serial.println("Message failed to send. Reconnecting to MQTT Broker and trying again");
      client.connect(mqtt_clientID,mqtt_username,mqtt_password);
      delay(10); // This delay ensures that client.publish doesn't clash with the client.connect call
      client.publish(mqtt_topic_temp, (char*)data.c_str());
    }
  }

}
