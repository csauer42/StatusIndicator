#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_LEDBackpack.h>

#define BRIGHTNESS 4
#define BAUDRATE 9600
#define ADDRESS 0x70

Adafruit_AlphaNum4 alpha4 = Adafruit_AlphaNum4();
char displaybuffer[4] = {' ', ' ', ' ', ' '};

void writeBuffer() {
  if (displaybuffer[0] == 0 &&
      displaybuffer[1] == 0 &&
      displaybuffer[2] == 0) {
    int value = displaybuffer[3];
    if (value >= 0 && value <= 15) {
      alpha4.setBrightness(value);
    }
  } else {
    alpha4.writeDigitAscii(0, displaybuffer[0]);
    alpha4.writeDigitAscii(1, displaybuffer[1]);
    alpha4.writeDigitAscii(2, displaybuffer[2]);
    alpha4.writeDigitAscii(3, displaybuffer[3]);
  }

  alpha4.writeDisplay();
}

void clearBuffer() {
  for (int i = 0; i < 4; i++) {
    displaybuffer[i] = ' ';
  }
}

void setup() {
  Serial.begin(BAUDRATE);
  alpha4.begin(ADDRESS);
  alpha4.clear();
  alpha4.setBrightness(BRIGHTNESS);
  alpha4.writeDisplay();
}

void loop() {
  int idx = 0;
  while (Serial.available() > 0) {
    char c = Serial.read();

    if (c == '\n') {
      idx = 0;
      writeBuffer();
      clearBuffer();
    } else if (idx < 4) {
      displaybuffer[idx] = c;
      idx++;
    }
  }
}
