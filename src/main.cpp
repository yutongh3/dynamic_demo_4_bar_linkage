#include <Arduino_FreeRTOS.h>
#include <Arduino.h>
#include <Servo.h>

const int servoPin = 9;
Servo myServo;
String command = "";
bool newCommand = false;

void vTaskServoControl(void *pvParameters);
void vTaskSerialRead(void *pvParameters);

void setup() {
  myServo.attach(servoPin);
  Serial.begin(9600);
  xTaskCreate(vTaskServoControl, "Servo Control", 100, NULL, 1, NULL);
  xTaskCreate(vTaskSerialRead, "Serial Read", 100, NULL, 1, NULL);
}

void loop() {
  // Empty loop as FreeRTOS tasks handle everything
}

void vTaskServoControl(void *pvParameters) {
  for (;;) {
    if (newCommand) {
      if (command == "Right") {
        myServo.write(0);
        Serial.println("Servo rotating clockwise");
      } else if (command == "Left") {
        myServo.write(180);
        Serial.println("Servo rotating counterclockwise");
      } else if (command == "Stop") {
        myServo.writeMicroseconds(1500);
      } else if (int(command.toInt()) >= 0 && int(command.toInt()) <= 100) {
        myServo.write(int(command.toInt()));
        Serial.println("Servo rotating to " + command + " degrees");
      } else {
        
        Serial.println("Invalid command");
      }
      newCommand = false;
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void vTaskSerialRead(void *pvParameters) {
  for (;;) {
    if (Serial.available() > 0) {
      command = Serial.readString();
      command.trim();
      newCommand = true;
    }
    vTaskDelay(100 / portTICK_PERIOD_MS);
  }
}
