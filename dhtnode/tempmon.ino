
/*
 *  This sketch demonstrates how to set up a simple HTTP-like server.
 *  The server will set a GPIO pin depending on the request
 *    http://server_ip/gpio/0 will set the GPIO2 low,
 *    http://server_ip/gpio/1 will set the GPIO2 high
 *  server_ip is the IP address of the ESP8266 module, will be 
 *  printed to Serial when the module is connected.
 */

#include <ESP8266WiFi.h>
#include "DHTesp.h"

const char* ssid = "InsidiousInternet";
const char* password = "superman";

// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(80);
DHTesp dht;

void setup() {
  Serial.begin(115200);
  Serial.println();
  

  dht.setup(3); // data pin 3
  
  delay(10);
    
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
  
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
  
  // Read the first line of the request
  String req = client.readStringUntil('\r');
  Serial.println(req);
  client.flush();
  
  
  if (req.indexOf("/get_temp_humid") != -1) {
    float humidity = dht.getHumidity();
    float temp = dht.getTemperature();
    Serial.println("Temperature (C)\tHumidity (%)");
    Serial.print(temp, 1);
    Serial.print("\t");
    Serial.print(humidity, 1);
    
    // Prepare the response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/json");
    client.println("");
    client.print("{\"temperature\":");
    client.print(temp);
    client.print(", \"humidity\":");
    client.print(humidity);
    client.print("}");
  }
  else {
    Serial.println("invalid request");
    client.stop();
    return;
  }

  client.flush();

  
  delay(1);
}

