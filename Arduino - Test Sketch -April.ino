int potPin = 2;
int ledPin = 13;
int val = 0;
float randnum = 0;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:

  randnum = random(0,1000) / 100.0;
  val = analogRead(potPin);
    
  Serial.print(val);
  Serial.print(",");
  Serial.println(randnum);

  delay(250);
  
}
