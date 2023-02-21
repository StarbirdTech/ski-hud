#include <Arduino.h>
#include <U8x8lib.h>
#include <Arduino_JSON.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

U8X8_SSD1306_128X64_NONAME_4W_SW_SPI u8x8(/* clock=*/ 13, /* data=*/ 11, /* cs=*/ 10, /* dc=*/ 7, /* reset=*/ 8);

int arr[3][2] = {{100,30},{90,90},{75,50}};

void setup(void)
{
  Serial.begin(1000000);
  Serial.write("Hello!");
  u8x8.begin();
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_f);
}

void loop(void) {
  // if (Serial.available() > 0) {
  //   JSONVar myArray = JSON.parse(Serial.read());

  //   u8x8.print("Hello");
  for (int i = 0; i < 3; i++) {
    int x = arr[i][0];
    int y = arr[i][1];
    //   Serial.write(x);
    u8x8.drawString(x, y, "X");
    delay(200);
  }
  u8x8.clear();
    // }
  //}
}

