//Defining pin setup for steering servo (motor A):
int enA = 5;
int in1 = 10;
int in2 = 11;

//Defining pin setup for prime mover (motor B):
int enB =  6;
int in3 = 12;
int in4 = 13;

int td = 30; //time delay in milliseconds
int motion = 0; //no motion in the start

int drivespeed = 160;
int steerspeed = 240;

void setup() {
  // setting pin modes
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  Serial.begin(115200);
}


void loop() {
  // checking for data availability at serial port:
  if (Serial.available()>0){
    motion = Serial.read();
  }

  else{
    stopMotors();
  }

}

//defining the motion functions:

void forward(int time){
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  analogWrite(enB, drivespeed);
  delay(td);
}

void reverse(int time){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, drivespeed);
  delay(td);
}

void left(int time){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  delay(td);
}

void right(int time){
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  delay(td);
}

void fleft(int time){
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  analogWrite(enB, drivespeed);
  delay(td);
}

void fright(int time){
  digitalWrite(in3, LOW);
  digitalWrite(in4, HIGH);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  analogWrite(enB, drivespeed);
  delay(td);
}

void Rleft(int time){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  analogWrite(enB, drivespeed);
  delay(td);
}

void Rright(int time){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, steerspeed);
  analogWrite(enB, drivespeed);
  delay(td);
}

void brake(int time){
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);
  analogWrite(enB, 20);
  delay(td);
}


void stopMotors(){
  digitalWrite(in3, LOW);
  digitalWrite(in4, LOW);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);
  analogWrite(enA, 0);
  analogWrite(enB, 0);
}

//the following function will decide which motion to call 
//based on the signal received from raspberry pi

void decide(int motion, int td){
  switch (motion){
    case 0: stopMotors; break;
    case 1: forward(td); break;
    case 2: reverse(td); break;
    case 3: left(td); break;
    case 4: right(td); break;
    case 5: fleft(td); break;
    case 6: fright(td); break;
    case 7: Rleft(td); break;
    case 8: Rright(td); break;
    case 9: brake(td); break;

    default: Serial.print("No motion commanded");
  }
}
