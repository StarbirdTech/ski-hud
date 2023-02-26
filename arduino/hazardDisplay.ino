#include <Arduino.h>
#include <U8x8lib.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

U8X8_SSD1306_128X64_NONAME_4W_SW_SPI u8x8(/* clock=*/ 13, /* data=*/ 11, /* cs=*/ 10, /* dc=*/ 7, /* reset=*/ 8);

int count = 0;
int* points = NULL; // Initialize the pointer to NULL

void setup() {
  Serial.begin(1000000);
  u8x8.begin();
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_f);
}

void loop() {
  if (Serial.available()) {
    int data = Serial.read();
    if (data == '\n') { // The end of the data has been reached
      // Allocate the array based on the number of elements received
      points = new int[count];
      u8x8.clear();
      // Read the data into the array
      for (int i = 0; i < count; i += 2) {
        int x = points[i];
        int y = points[i+1];
        u8x8.drawString(x, y, "!");
      }
      
      // Free the memory allocated for the array
      delete[] points;
      
      // Reset the count
      count = 0;
    } else {
      points[count] = Serial.parseInt();
      count++;
    }
  }
}
