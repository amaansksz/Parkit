#include <Firebase_ESP_Client.h>
#include <Servo.h>
#include <ESP8266WiFi.h>
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define FIREBASE_HOST "parkit-ebd49-default-rtdb.firebaseio.com"
// #define FIREBASE_AUTH "GpamTpBd2McYQT9B2oXNBHqycph1fEdSt2FvMJTx"
#define FIREBASE_AUTH "AIzaSyChMCs0vC1InLHKdJsQy4xGfK-gzZAtzPA"

#define ssid "Narzo 70pro"
#define password "Tanuu12345"

#define SERVO_PIN D1

Servo servo;

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

bool signupOK=false;

void setup() {
  Serial.begin(115200);
  delay(10);

  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  config.api_key=FIREBASE_AUTH;
  config.database_url=FIREBASE_HOST;

  if(Firebase.signUp(&config, &auth, "", "")){
    Serial.println("signUp OK");
    signupOK=true;
  }else{
    Serial.println("signUp errrrrrrrrr");
    // Serial.println("%s\n", config.signer.signupError.message.c_str());
  }

  config.token_status_callback=tokenStatusCallback;

  Firebase.begin(&config, &auth);

  servo.attach(SERVO_PIN);
}

void loop() {
  if (Firebase.ready()) {
    Serial.println("Firebase connected");
    
    // Read data from Firebase
    if (Firebase.RTDB.getBool(&fbdo, "gate")) {
      bool gateOpen = fbdo.boolData();

      if (gateOpen) {
        servo.write(180); 
        Serial.println("Gate is open");
        
        // Update gate state in Firebase
        Firebase.RTDB.setBool(&fbdo, "gate", false);
      } else {
        // Close the gate if it has been open for more than 3 seconds
        static unsigned long gateOpenTime = millis();
        if (millis() - gateOpenTime >= 3000) {
          servo.write(0);
          Serial.println("Gate is closed");
          // Firebase.RTDB.setBool(&fbdo, "gate", true);

        }
      }
    } else {
      Serial.println("Failed to get gate state from Firebase");
    }
  } else {
    Serial.println("Firebase not connected");
  }

  delay(3000);
}
