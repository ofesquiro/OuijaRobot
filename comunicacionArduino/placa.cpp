#include <Servo.h>

Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;

struct Letra{
    int gradosServo1;
    int gradosServo2;
    int gradosServo3; 
    int gradosServo4;
};

void asignarGrados(Letra letra);

void setup() {
      servo1.attach(A1);
      servo1.write(0);

    servo2.attach(A2);
    servo2.write(0);

    servo3.attach(A3);
    servo3.write(0);

    servo4.attach(A4);
    servo4.write(0);
}

void asignarGrados(Letra letra) {
	servo1.write(letra.gradosServo1);
}

void loop() {
    Letra a = {20, 20, 20, 20};
    Letra b = {40, 40, 40, 40};
    Letra c = {60, 60, 60, 60};
  
    servo1.write(a.gradosServo1);
    servo2.write(a.gradosServo2);
    servo3.write(a.gradosServo3);
    servo4.write(a.gradosServo4);
    delay(2000);
  
    servo1.write(b.gradosServo1);
    servo2.write(b.gradosServo2);
    servo3.write(b.gradosServo3);
    servo4.write(b.gradosServo4);
    delay(2000);
  
    servo1.write(c.gradosServo1);
    servo2.write(c.gradosServo2);
    servo3.write(c.gradosServo3);
    servo4.write(c.gradosServo4);
    delay(1000);
  
  asignarGrados(a);
}