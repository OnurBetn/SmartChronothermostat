#include <ESP8266WiFi.h>
#include <PubSubClient.h>

#define relayPin D6

const char* ssid = "WebPocket-6C3E";
const char* password = "Q39EDNG9";
const char* mqttServer = "192.168.1.100";
const int mqttPort = 1883;
const char* mqttUser = "YourMqttUser";
const char* mqttPassword = "YourMqttUserPassword";
char* status = "OFF";

WiFiClient espClient;
PubSubClient client(espClient);


void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP8266Client-1")) {
      
      Serial.println("connected");  
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }

  client.subscribe("rooms/kitchen/relay");
 
}
void callback(char* topic, byte* payload, unsigned int length) {
 
  Serial.print("Message arrived in topic: ");
  Serial.println(topic);
  Serial.print(status[1]);
 
  Serial.print("Message:");
    if (payload[1]=='N' && status[1]=='F')
    {
      digitalWrite(relayPin, HIGH);
      Serial.println("on");
      }
    else {
      if(payload[1]=='F'&& status[1]=='N'){
         digitalWrite(relayPin, LOW);
         Serial.println("off");
        }
  }
    status[1]=payload[1];
 
  Serial.println();
  Serial.println("-----------------------");
 
}
void loop() {
  client.loop();
  delay(1000);
}
