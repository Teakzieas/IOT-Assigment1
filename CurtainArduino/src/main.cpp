#include <Arduino.h>
#include <AccelStepper.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define STEP_PIN 6
#define DIR_PIN 7
#define DHTPIN 4
#define DHTTYPE DHT11

const int stepsPerRevolution = 200*16;
const long totalSteps = 86400;

AccelStepper stepper(1, STEP_PIN, DIR_PIN);
DHT_Unified dht(DHTPIN, DHTTYPE);

unsigned long previousMillis = 0;
static unsigned long lastSendMillis = 0;
const long interval = 2000;

int lightOut = 1023;
int lightIn = 1023;
float temp = 25.0;
float humidity = 60.0;

int curtainPos = 0;
int lastCurtainPos = 0;

void setup()
{
  Serial.begin(115200);
  stepper.setMaxSpeed(200000);
  stepper.setAcceleration(100000);
  pinMode(2, INPUT_PULLUP);
  while (digitalRead(2) == HIGH) {
    stepper.setSpeed(-50000);
    stepper.runSpeed();
  }
  stepper.stop();
  stepper.setCurrentPosition(0);
  dht.begin();
  Serial.println(F("DHT11 Sensor Initialized"));
}

void loop()
{
  if (Serial.available() > 0) {
    int incomingValue = Serial.parseInt();
    while (Serial.available() > 0) {
      Serial.read();
    }
    if (incomingValue >= 0 && incomingValue <= 100) {
      curtainPos = incomingValue;
    }
  }

  if (curtainPos != lastCurtainPos) {
    lastCurtainPos = curtainPos;
    long targetPosition = map(curtainPos, 0, 100, 0, 86400);
    stepper.moveTo(targetPosition);
    Serial.println("Moving to position: " + String(targetPosition));
  }
  stepper.runToPosition();

  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval)
  {
    previousMillis = currentMillis;
    sensors_event_t tempEvent, humidityEvent;
    dht.temperature().getEvent(&tempEvent);
    dht.humidity().getEvent(&humidityEvent);

    temp = tempEvent.temperature;
    humidity = humidityEvent.relative_humidity;

    lightOut = 1023 - analogRead(5);
    lightIn = 1023 - analogRead(0);
  }
  
  if (currentMillis - lastSendMillis >= 1000) {
    lastSendMillis = currentMillis;
    Serial.println("S|" + String(curtainPos) + "|" + String(lightIn) + "|" + String(lightOut) + "|" + String(temp) + "|" + String(humidity) + "|E");
  }
}
