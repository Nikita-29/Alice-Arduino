#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <Adafruit_NeoPixel.h>

#define MATRIX_PIN    5
#define LED_COUNT 16

const char* ssid = "GoTo";
const char* password = "11110011";
const char* host = "35.237.0.149";
const int httpsPort = 443;
const char* fingerprint = "7f 22 e6 ca bb 4e 10 00";

int p;
int p2;
int x;
Adafruit_NeoPixel matrix = Adafruit_NeoPixel(LED_COUNT, MATRIX_PIN, NEO_GRB + NEO_KHZ800);

void colorWipe(uint32_t c, uint8_t wait)
{
  for (uint16_t i = 0; i < matrix.numPixels(); i++) {
    matrix.setPixelColor(i, c);
    matrix.show();
    delay(wait);
  }
  
}

void colorWipe2(uint32_t c, uint8_t wait){
  for (uint16_t i=0;i<=(matrix.numPixels()/2);i++){
    matrix.setPixelColor(i,c);
    matrix.show();
    matrix.setPixelColor((matrix.numPixels()-i),matrix.Color(0,p2,p2));
    matrix.show();
    delay(wait);
  }
}

void colorWipe3(uint32_t c,uint16_t wait){
  for(uint16_t i=0;i<=(matrix.numPixels()/2);i++){
    matrix.setPixelColor(i,(matrix.Color(p2,p2,0)));
    matrix.show();
    matrix.setPixelColor((matrix.numPixels()-i),c);
    matrix.show();
    delay(wait);
  }
}


void setup(){
  pinMode(A0,INPUT);
  matrix.begin();
  Serial.begin(9600);
  Serial.println();
  Serial.print("connecting to ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  




  
}


void loop(){
  
    p=analogRead(A0);
    p2=map(p,0,1023,0,255);
    WiFiClientSecure client;
    Serial.print("connecting to ");
    Serial.println(host);
    if (!client.connect(host, httpsPort)) {
      Serial.println("connection failed");
      return;
    }

    if (client.verify(fingerprint, host)) {
      Serial.println("certificate matches");
    }   else {
      Serial.println("certificate doesn't match");
    }

    String url = "/get_status";
    Serial.print("requesting URL: ");
    Serial.println(url);

    client.print(String("GET ") + url + " HTTP/1.1\r\n" +
                "Host: " + host + "\r\n" +
                "User-Agent: BuildFailureDetectorESP8266\r\n" +
                "Connection: close\r\n\r\n");

    Serial.println("request sent");
    while (client.connected()) {
      String line = client.readStringUntil('\n');
      Serial.println(line);
      if (line == "\r") {
        Serial.println("headers received");
        break;
      }
    }
    
    String line = client.readStringUntil('\n');
    int x=line.toInt();
    Serial.println(line);
 

  if (x==0){
    colorWipe(matrix.Color(0,0,0),70);
    
  }
  if (x==1){
    for(int i=0;i<4;i++){
      colorWipe(matrix.Color(p2,0,0),30);
      colorWipe(matrix.Color(0,0,0),50);
    }
    colorWipe(matrix.Color(p2,0,0),30);
    
  }
  if (x==2){
    for(int i=0;i<4;i++){
      colorWipe(matrix.Color(0,0,p2),30);
      colorWipe(matrix.Color(0,0,0),50);
    }
    colorWipe(matrix.Color(0,0,p2),50);    
  }
  if(x==3){
    for(int i=0;i<4;i++){
      colorWipe3(matrix.Color(p2,0,p2),30);
      colorWipe(matrix.Color(0,0,0),50);
    }
    colorWipe(matrix.Color(p2,0,p2),50);
  }
  if(x==4){
    for(int i=0;i<5;i++){
        colorWipe(matrix.Color(p2, 0, 0), 50);
        colorWipe(matrix.Color(0, p2, 0), 50);
        colorWipe(matrix.Color(0, 0, p2), 50);
        colorWipe(matrix.Color(0, 0, 0), 50);
      }
    colorWipe(matrix.Color(p2,p2,p2),70);
    
  }
  if(x==5){
    for(int i=0;i<5;i++){
        colorWipe2(matrix.Color(p2,p2,0),300);
        colorWipe(matrix.Color(0,0,0),50);
        colorWipe2(matrix.Color(p2,0,p2),300);
        delay(100);
    }
    
  }
  
  
  
}

