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
  // if max array size is available in the buffer, read it into the array using parseInt
  if (Serial.available() >= maxArraySize*2)
  {
    for (int i = 0; i < maxArraySize/2; i++)
    {
      u8g2.drawDisc(Serial.parseInt(), Serial.parseInt(), 2);
    }
    u8g2.sendBuffer();
    u8g2.clearBuffer();
    //cooldown = 10;
    //u8g2.sendBuffer();
    //u8g2.clearBuffer();
  }
  // else if (cooldown > 0)
  // {
  //   cooldown--;
  // }
  // else
  // {
  //   for (int i = 0; i < maxArraySize; i += 2)
  //   {
  //     u8g2.drawDisc(myArray[i], myArray[i + 1], 1);
      
  //     if (random(500) == 0)
  //     {
  //       myArray[i] = random(128);
  //       myArray[i + 1] = random(64);
  //     }
  //     else if (random(100) < 10)
  //     {
  //       // if near the edge of the screen, move in the opposite direction
  //       // otherwise, move in a random direction
  //       if (myArray[i] < 5)
  //       {
  //         myArray[i] += random(5);
  //       }
  //       else if (myArray[i] > 123)
  //       {
  //         myArray[i] -= random(5);
  //       }
  //       else
  //       {
  //         myArray[i] += random(-5, 5);
  //       }
  //       if (myArray[i + 1] < 5)
  //       {
  //         myArray[i + 1] += random(5);
  //       }
  //       else if (myArray[i + 1] > 59)
  //       {
  //         myArray[i + 1] -= random(5);
  //       }
  //       else
  //       {
  //         myArray[i + 1] += random(-5, 5);
  //       }
  //     }
  //   }
  //   u8g2.sendBuffer();
  //   u8g2.clearBuffer();
  // }
}
