#include <U8g2lib.h>
#include <SPI.h>

U8G2_SSD1306_128X64_NONAME_F_4W_SW_SPI u8g2(U8G2_R0, /* clock=*/13, /* data=*/11, /* cs=*/10, /* dc=*/7, /* reset=*/8);

void setup()
{
  Serial.begin(9600);
  u8g2.begin();
}

int point[2];
int count = 0;

void loop()
{
  if (Serial.available())
  {
    int input = Serial.parseInt();

    if (input == 0) {
      u8g2.sendBuffer();
      u8g2.clearBuffer();
      return;
    }

    point[count] = input;
    count++;
    if (count == 2)
    {
      u8g2.drawDisc(point[0], point[1], 2);
      count = 0;
    }
  }
}