#include <Servo.h>

Servo myservo;  

int pos = 0;    // variable to store the servo position
String  str = "";
int num = -1;
int corner = -1;
int serv2=90;
int serv3=90;
int serv4=90;
int serv5=90;
int serv6=90;
int serv7=90;
void setup() {
  // put your setup code here, to run once:
 Serial.begin(9600);
 Serial.println("Hello Computer");
 pinMode(LED_BUILTIN, OUTPUT);
 str.reserve(200);
}

void loop() {
  // put your main code here, to run repeatedly:

}
void serialEvent()
{
  str = "";
  if (Serial.available()) 
  {
    str = Serial.readString();
 //   Serial.print (str);
 //   Serial.print (str.length());
    Func1 (str);
    srvo ();
  }
}

void Func1 (String st)
{

  String st1="";
  String st2="";
  num = 0;
  corner = 0;
  for (int i = 0; i < str.length()-1; i++)
  {
    if (str[i] != ' ')
      st1 += str[i];
    else 
    {
      while (str[i] == ' ' )
      i++;
      while (i<(str.length()-1))
      {
       st2+=str[i];
       i++;
      }
    }
  }
  num = st1.toInt();
  corner = st2.toInt(); 
   Serial.print (num);
   Serial.print ("  ");
   Serial.print (corner);
   Serial.print ("\n");
  
}

void srvo ()
{
  int start = 0;
                                                                                                                                                                                                                                                                                                                                                             
   if (num == 2)
  {
    start = serv2;
    serv2 = corner;
   }
   if (num == 3)
  {
    start = serv3;
    serv3 = corner;
   }
   if (num == 4)
  {
    start = serv4;
    serv4 = corner;
   }
   if (num == 5)
  {
    start = serv5;
    serv5 = corner;
   }
   if (num == 6)
  {
    start = serv6;
    serv6 = corner;
   }
   if (num == 7)
  {
    start = serv7;
    serv7 = corner;
   }
   myservo.attach(num);  // attaches the servo on pin 9 to the servo object
   //int start = myservo.read();
   Serial.print ("stasrt");
   Serial.print (start);
   Serial.print ("\n");
   if (corner < start)
   for (pos = start; pos >= corner; pos -= 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(30);                       // waits 15ms for the servo to reach the position
   }
  else 
  for (pos = start; pos <= corner; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(30);                       // waits 15ms for the servo to reach the position
  } 
}
