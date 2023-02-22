#include <Arduino.h>
#include <U8x8lib.h>

#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

U8X8_SSD1306_128X64_NONAME_4W_SW_SPI u8x8(/* clock=*/ 13, /* data=*/ 11, /* cs=*/ 10, /* dc=*/ 7, /* reset=*/ 8);

int arr[3][2] = {{100,30},{90,90},{75,50}};

void setup()
{
  Serial.begin(1000000);
  Serial.write("Hello!");
  u8x8.begin();
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_f);
}

void loop() {
  for (int i = 0; i < 3; i++) {
    u8x8.drawString(arr[i][0], arr[i][1], "!");
    delay(200);
  }
  u8x8.clear();
}
