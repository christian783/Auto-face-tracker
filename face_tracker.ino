#include <Stepper.h>

#define STEPS 2048  // steps per revolution for 28BYJ-48

Stepper stepper(STEPS, 8, 10, 9, 11);

char command;

void setup() {
  Serial.begin(9600);
  stepper.setSpeed(10); // RPM
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();

    if (command == 'L') {
      stepper.step(-10); // rotate left
    } 
    else if (command == 'R') {
      stepper.step(10);  // rotate right
    }
    else if (command == 'S') {
      // stop (do nothing)
    }
  }
}
