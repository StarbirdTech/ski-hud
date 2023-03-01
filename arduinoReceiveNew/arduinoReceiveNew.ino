#include <U8g2lib.h>
#include <SPI.h>

U8G2_SSD1306_128X64_NONAME_F_4W_SW_SPI u8g2(U8G2_R0, /* clock=*/13, /* data=*/11, /* cs=*/10, /* dc=*/7, /* reset=*/8);

#define maxArraySize 12

uint16_t myArray[maxArraySize];

int cooldown = 0;

void setup()
{
  Serial.begin(9600);
  u8g2.begin();
}

void loop()
{
  if (Serial.available() >= maxArraySize*2)
  {
    for (int i = 0; i < maxArraySize/2; i++)
    {
      u8g2.drawDisc(Serial.parseInt(), Serial.parseInt(), 2);
    }
    u8g2.sendBuffer();
    u8g2.clearBuffer();
    }
}
