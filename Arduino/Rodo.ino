#include <Thread.h>
#include <Servo.h>

Servo myservo; 
Thread ReportThread = Thread(); // создаём поток для отправки состояния руки

String  str = "";  // строка для обработки команд для сервоприводов (Func1)
int num = -1;  //номера сервопривода
int corner = -1;  //угол на который необходимо повернуть серво
bool ready = true;   //состояние руги готов принимать координаты/нахожусь в движении
// переменные для запоминания последних положений сервоприводов
int serv2=90;
int serv3=90;
int serv4=90;
int serv5=90;
int serv6=90;
int serv7=90;

void setup() {
  Serial.begin(9600);
  str.reserve(200);
  ReportThread.onRun(Report);  // назначаем потоку задачу
    ReportThread.setInterval(1000); // задаём интервал срабатывания, мсек
    Serial.println("Start!");
}

void loop() {
  // put your main code here, to run repeatedly:
  if (ReportThread.shouldRun())
        ReportThread.run(); // запускаем поток
}

//Функция отправки состояния на ПК
void Report() { 
    if (ready)
      Serial.println("2");
      else Serial.println("1");
}

//Прерывание после получаения команд
void serialEvent()
{
  ready = false;
  str = "";
  if (Serial.available()) 
  {
    str = Serial.readString();
    Func1 (str);
    srvo ();
  }
}

//Функция для обработки принятой по Serial port строки 
void Func1 (String st)
{
  String st1="";
  String st2="";
  num = 0;
  corner = 0;
  if (st == "")
    {
      Serial.println("4");
      Serial.println(st);
      ready = true;
      return 0;
    }
  for (int i = 0; i < str.length(); i++)
  {
    if (st[i] != ' ')
      st1 += st[i];
    else 
    {
      while (st[i] == ' ' )
      i++;
      while (i<(str.length()))
      {
       st2+=st[i];
       i++;
      }
    }
  }
  num = st1.toInt();
  corner = st2.toInt(); 
  if (num<2 || num>7|| corner<0 ||corner >180 )
  {
    Serial.println("4");
    Serial.println(st);
      ready = true;
      return 0;
  
  }
  else  Serial.println("3");
  Serial.print (num);
   Serial.print ("  ");
   Serial.print (corner);
   Serial.print ("\n");
}
// функция для установки сервопривода в заданное положение
void srvo ()
{
  if (ready)
    return 0;
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
   myservo.attach(num);  // attaches the servo to the servo object
   int pos = 0;    // переменная для позиции в цикле
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
  ready = true;
}