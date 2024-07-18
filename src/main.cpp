#include <Arduino.h>
#include <Servo.h>
#include <Arduino_FreeRTOS.h>
#include <AS5600.h>

const int servoPin = 17;
const int DirPin = 16;
Servo myServo;
AS5600L as5600; // I2C address 0x36

int cwMaxDuty = 60;
int cwMidDuty = 70;
int cwMinDuty = 80;

int ccwMaxDuty = 120;
int ccwMidDuty = 110;
int ccwMinDuty = 100;

int stopDuty = 90;

int deg;
int oldDeg;
bool rowOver = false;

String command = "";

void vTaskSerialRead(void *pvParameters);

void setup() {
  pinMode(servoPin, OUTPUT);
  myServo.attach(servoPin);
  myServo.write(stopDuty);
  Serial.begin(115200);
  Serial.println("Board initialized");
  as5600.begin(DirPin);
  as5600.setDirection(AS5600_CLOCK_WISE);
  as5600.setAddress(0x36);
  Serial.println("Encoder initialized");
  xTaskCreate(vTaskSerialRead, "Serial Read", 256, NULL, 1, NULL);
}

void loop() {
}

void vTaskSerialRead(void *pvParameters) {
  for (;;) {
    if (Serial.available() > 0) {
      command = Serial.readString();
      command.trim();
      if (command == "CW 50") {
        myServo.write(cwMinDuty);
      } else if (command == "CW 75") {
        myServo.write(cwMidDuty);
      } else if (command == "CW 100") {
        myServo.write(cwMaxDuty);
      } else if (command == "CCW 50") {
        myServo.write(ccwMinDuty);
      } else if (command == "CCW 75") {
        myServo.write(ccwMidDuty);
      } else if (command == "CCW 100") {
        myServo.write(ccwMaxDuty);
      } else if (command == "STOP") {
        myServo.write(stopDuty);
      } else if (command == "0deg") {
        deg = as5600.readAngle();
        myServo.write(cwMaxDuty);
        while (deg > 1990 || deg < 1980) {
          deg = as5600.readAngle();
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        myServo.write(stopDuty);
      } else if (command == "90deg") {
        deg = as5600.readAngle();
        myServo.write(cwMaxDuty);
        while (deg > 980 || deg < 970) {
          deg = as5600.readAngle();
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        myServo.write(stopDuty);
      } else if (command == "180deg") {
        deg = as5600.readAngle();
        myServo.write(cwMaxDuty);
        while (deg > 4050 || deg < 4040) {
          deg = as5600.readAngle();
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        myServo.write(stopDuty);
      } else if (command == "270deg") {
        deg = as5600.readAngle();
        myServo.write(cwMaxDuty);
        while (deg > 2980 || deg < 2960) {
          deg = as5600.readAngle();
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        myServo.write(stopDuty);
      } else if (command == "forward") {
        oldDeg = as5600.readAngle();
        if (oldDeg < 100) {
          rowOver = true;
        }
        deg = as5600.readAngle();
        myServo.write(cwMaxDuty);
        while (oldDeg - deg < 100) {
          deg = as5600.readAngle();
          if (rowOver && deg > 800) deg -= 4200;
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        if (rowOver) rowOver = false;
        myServo.write(stopDuty);
      } else if (command == "backward") {
        oldDeg = as5600.readAngle();
        Serial.println(oldDeg);
        if (oldDeg > 3995) {
          rowOver = true;
        }
        deg = as5600.readAngle();
        myServo.write(ccwMaxDuty);
        while (deg - oldDeg < 100) {
          deg = as5600.readAngle();
          if (rowOver && deg < 1200) deg += 4200;
          vTaskDelay(10 / portTICK_PERIOD_MS);
        }
        if (rowOver) rowOver = false;
        myServo.write(stopDuty);
      } else {
        Serial.println("Invalid command");
      }
    }
    // Serial.println(as5600.readAngle());
    vTaskDelay(5 / portTICK_PERIOD_MS);
  }
}

