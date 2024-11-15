// Define pins for front motors (IC1)
const int leftFrontMotorPin1 = 9;
const int leftFrontMotorPin2 = 10;
const int rightFrontMotorPin1 = 11;
const int rightFrontMotorPin2 = 12;

// Define pins for rear motors (IC2)
const int leftRearMotorPin1 = 5;
const int leftRearMotorPin2 = 6;
const int rightRearMotorPin1 = 7;
const int rightRearMotorPin2 = 8;

const int EN_PIN = 3;

void setup() {
  pinMode(EN_PIN, OUTPUT);
  // Set motor control pins as outputs
  pinMode(leftFrontMotorPin1, OUTPUT);
  pinMode(leftFrontMotorPin2, OUTPUT);
  pinMode(rightFrontMotorPin1, OUTPUT);
  pinMode(rightFrontMotorPin2, OUTPUT);

  pinMode(leftRearMotorPin1, OUTPUT);
  pinMode(leftRearMotorPin2, OUTPUT);
  pinMode(rightRearMotorPin1, OUTPUT);
  pinMode(rightRearMotorPin2, OUTPUT);
  digitalWrite(EN_PIN, HIGH);
  Serial.begin(9600);
  Serial1.begin(38400);
}

// Function to stop all motors
void stopMotors() {
  digitalWrite(leftFrontMotorPin1, LOW);
  digitalWrite(leftFrontMotorPin2, LOW);
  digitalWrite(rightFrontMotorPin1, LOW);
  digitalWrite(rightFrontMotorPin2, LOW);

  digitalWrite(leftRearMotorPin1, LOW);
  digitalWrite(leftRearMotorPin2, LOW);
  digitalWrite(rightRearMotorPin1, LOW);
  digitalWrite(rightRearMotorPin2, LOW);
}

// Function for forward motion
void moveForward() {
  digitalWrite(leftFrontMotorPin1, LOW);
  digitalWrite(leftFrontMotorPin2, HIGH);
  digitalWrite(rightFrontMotorPin1, LOW);
  digitalWrite(rightFrontMotorPin2, HIGH);

  digitalWrite(leftRearMotorPin1, HIGH);
  digitalWrite(leftRearMotorPin2, LOW);
  digitalWrite(rightRearMotorPin1, HIGH);
  digitalWrite(rightRearMotorPin2, LOW);
}

// Function for backward motion
void moveBackward() {
  digitalWrite(leftFrontMotorPin1, HIGH);
  digitalWrite(leftFrontMotorPin2, LOW);
  digitalWrite(rightFrontMotorPin1, HIGH);
  digitalWrite(rightFrontMotorPin2, LOW);

  digitalWrite(leftRearMotorPin1, LOW);
  digitalWrite(leftRearMotorPin2, HIGH);
  digitalWrite(rightRearMotorPin1, LOW);
  digitalWrite(rightRearMotorPin2, HIGH);
}

// Function for turning left
void turnLeft() {
  digitalWrite(leftFrontMotorPin1, HIGH);
  digitalWrite(leftFrontMotorPin2, LOW);
  digitalWrite(rightFrontMotorPin1, LOW);
  digitalWrite(rightFrontMotorPin2, HIGH);

  digitalWrite(leftRearMotorPin1, LOW);
  digitalWrite(leftRearMotorPin2, HIGH);
  digitalWrite(rightRearMotorPin1, HIGH);
  digitalWrite(rightRearMotorPin2, LOW);
}

// Function for turning right
void turnRight() {
  digitalWrite(leftFrontMotorPin1, LOW);
  digitalWrite(leftFrontMotorPin2, HIGH);
  digitalWrite(rightFrontMotorPin1, HIGH);
  digitalWrite(rightFrontMotorPin2, LOW);

  digitalWrite(leftRearMotorPin1, HIGH);
  digitalWrite(leftRearMotorPin2, LOW);
  digitalWrite(rightRearMotorPin1, LOW);
  digitalWrite(rightRearMotorPin2, HIGH);
}

void bluetoothListen() {
  // Serial.println("hello");
  if(Serial1.available()){
    String command = Serial1.readStringUntil('\n');
    Serial.print("Received: ");
    Serial.println(command);
//    TODO: Where logic for control will come in
  }else{
    Serial.println("Bluetooth not connected");
  }
}

void loop() {
  // Example movement sequence
  // moveForward();
  // moveBackward();
  // turnLeft();
  // turnRight();
  bluetoothListen();
}