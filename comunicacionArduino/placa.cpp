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
	servo1.write(letra.gradosServo2);
	servo1.write(letra.gradosServo3);
	servo1.write(letra.gradosServo4);
}

void loop() {
    Letra a = {20, 20, 20, 20};
    Letra b = {40, 40, 40, 40};
    Letra c = {60, 60, 60, 60};
  
    asignarGrados(a);
    delay(2000);
    asignarGrados(b);
    delay(2000);
    asignarGrados(c);
    delay(1000);
}