#include <Arduino_FreeRTOS.h>
#include <Arduino.h>
#include <Servo.h>

const int servoPin = 9;
Servo myServo;
String command = "";
bool newCommand = false;

int dir = 0; // 0 = stop, 1 = right, 2 = left
int speed = 0;

void servoControl();
void vTaskSerialRead(void *pvParameters);

void setup() {
  myServo.attach(servoPin);
  myServo.write(90);
  Serial.begin(115200);
  xTaskCreate(vTaskSerialRead, "Serial Read", 100, NULL, 1, NULL);
}

void loop() {
  // Empty loop as FreeRTOS tasks handle everything
}

void servoControl() {
  if (dir == 1) {
    myServo.write(90 - speed);
  } else if (dir == 2) {
    myServo.write(90 + speed);
  } else {
    myServo.write(90);
  }
}

void vTaskSerialRead(void *pvParameters) {
  for (;;) {
    if (Serial.available() > 0) {
      command = Serial.readString();
      command.trim();
      if (command == "CW") {
        dir = 1;
      } else if (command == "CCW") {
        dir = 2;
      } else if (command == "Stop") {
        dir = 0;
      } else if (int(command.toInt()) >= 0 && int(command.toInt()) <= 100) {
        speed = int(command.toInt() * 0.3);
        Serial.println("Speed: " + String(speed));
      } else {
        Serial.println("Invalid command");
      }
      servoControl();
    }
    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}
