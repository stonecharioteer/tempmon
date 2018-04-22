#include <ESP8266WiFi.h>
#include "DHTesp.h"

const char* ssid = "SSIDHERE";
const char* password = "PASSWORDHERE";

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);
DHTesp dht;

void setup() {
  dht.setup(3); // data pin 3
  
  delay(10);
    
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  // Start the server
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  
  // Wait until the client sends some data
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');
  client.flush();
  
  
  if (req.indexOf("/temperature") != -1) {
    float temp = dht.getTemperature();
    // Prepare the response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/json");
    client.println("");
    client.print("{\"temperature\":");
    client.print(temp);
    client.print("}");
  }
  else if (req.indexOf("/humidity") != -1 ) {
    float humidity = dht.getHumidity();
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/json");
    client.println("");
    client.print("{\"humidity\":");
    client.print(humidity);
    client.print("}");
  }
  else if (req.indexOf("/whoami") != -1) {
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/json");
    client.println("");
    client.print("{\"id\":");
    client.print("\"IDHERE\"");
    client.print(", \"type\":");
    client.print("\"nodemcu\"");
    client.print("}");
  }
  else {
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/json");
    client.println("");
    client.print("{\"message\":");
    client.print("\"Unrecognized query\"");
    client.print("}");
    client.stop();
    return;
  }
  client.flush();
  delay(1);
}

