int **myArray;       // Pointer to a two-dimensional array
int arrayLength;     // Number of tuples in the array
int tupleLength = 2; // Number of integers in each tuple

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available())
  {
    // Read the string from serial
    String stringReceived = Serial.readStringUntil('\n');

    // Count the number of tuples in the string
    arrayLength = countChar(stringReceived, ',') / tupleLength + 1;

    // Allocate memory for the array
    myArray = new int *[arrayLength];
    for (int i = 0; i < arrayLength; i++)
    {
      myArray[i] = new int[tupleLength];
    }

    // Split the string into individual values
    int valueIndex = 0;
    for (int i = 0; i < arrayLength; i++)
    {
      for (int j = 0; j < tupleLength; j++)
      {
        int delimiterIndex = stringReceived.indexOf(',', valueIndex);
        if (delimiterIndex < 0)
        {
          break;
        }
        myArray[i][j] = atoi(stringReceived.substring(valueIndex, delimiterIndex).c_str());
        valueIndex = delimiterIndex + 1;
      }
      if (valueIndex >= stringReceived.length())
      {
        break;
      }
    }

    // Do something with the array of integers
    for (int i = 0; i < arrayLength; i++)
    {
      // Print the i-th element of the array
      Serial.print("(");
      for (int j = 0; j < tupleLength; j++)
      {
        Serial.print(myArray[i][j]);
        if (j < tupleLength - 1)
        {
          Serial.print(",");
        }
      }
      Serial.print(") ");
    }
    Serial.println();

    // Free the memory allocated for the array
    for (int i = 0; i < arrayLength; i++)
    {
      delete[] myArray[i];
    }
    delete[] myArray;
  }
}

// Function to count the number of occurrences of a character in a string
int countChar(String str, char c)
{
  int count = 0;
  for (int i = 0; i < str.length(); i++)
  {
    if (str.charAt(i) == c)
    {
      count++;
    }
  }
  return count;
}
