// Define inputs
#define serial0 1
#define serial1 2
#define retOff 3
#define retPos1 4
#define retPos2 5
#define retPos3 6
#define retPos4 7
#define engBrk 8
#define lgtOff 9
#define lgtPrk 10
#define lgtLow 11
#define lgtHgh 12
#define blnLft 12
#define blnRgt 14
#define wipOff 15
#define wipSpd1 16
#define wipSpd2 17
#define wipSpd3 18
#define elcOff 19
#define elcIgn 20
#define engSrt 21
#define trdWhl 22
#define lgtBcn 23
#define lgtHzd 24
#define difLoc 25
#define hndBrk 26
#define winLdn 27
#define winLup 28
#define winRdn 29
#define winRup 30

// Define outputs
#define indLgtPrk 31
#define indLgtLow 32
#define indLgtHgh 33
#define indBlnLft 34
#define indBlnRgt 35
#define indLgtBcn 36
#define indDifLoc 37
#define indHndBrk 38
#define indNoChrg 39
#define indNoOilp 40

String msg;

void pinIo(int pin, String msgOn, String msgOff){

  if (msg == msgOn) {
    digitalWrite(pin, HIGH);
  } else if (msg == msgOff) {
    digitalWrite(pin, LOW);
  }

}

void setup() {

  // pin setup
  pinMode(retOff, INPUT_PULLUP);
  pinMode(retPos1, INPUT_PULLUP);
  pinMode(retPos2, INPUT_PULLUP);
  pinMode(retPos3, INPUT_PULLUP);
  pinMode(retPos4, INPUT_PULLUP);
  pinMode(engBrk, INPUT_PULLUP);
  pinMode(lgtOff, INPUT_PULLUP);
  pinMode(lgtPrk, INPUT_PULLUP);
  pinMode(lgtLow, INPUT_PULLUP);
  pinMode(lgtHgh, INPUT_PULLUP);
  pinMode(blnLft, INPUT_PULLUP);
  pinMode(blnRgt, INPUT_PULLUP);
  pinMode(wipOff, INPUT_PULLUP);
  pinMode(wipSpd1, INPUT_PULLUP);
  pinMode(wipSpd2, INPUT_PULLUP);
  pinMode(wipSpd3, INPUT_PULLUP);
  pinMode(elcOff, INPUT_PULLUP);
  pinMode(elcIgn, INPUT_PULLUP);
  pinMode(engSrt, INPUT_PULLUP);
  pinMode(trdWhl, INPUT_PULLUP);
  pinMode(lgtBcn, INPUT_PULLUP);
  pinMode(lgtHzd, INPUT_PULLUP);
  pinMode(difLoc, INPUT_PULLUP);
  pinMode(hndBrk, INPUT_PULLUP);
  pinMode(winLdn, INPUT_PULLUP);
  pinMode(winLup, INPUT_PULLUP);
  pinMode(winRdn, INPUT_PULLUP);
  pinMode(winRup, INPUT_PULLUP);
  pinMode(indLgtPrk, OUTPUT);
  pinMode(indLgtLow, OUTPUT);
  pinMode(indLgtHgh, OUTPUT);
  pinMode(indBlnLft, OUTPUT);
  pinMode(indBlnRgt, OUTPUT);
  pinMode(indLgtBcn, OUTPUT);
  pinMode(indDifLoc, OUTPUT);
  pinMode(indHndBrk, OUTPUT);
  pinMode(indNoChrg, OUTPUT);
  pinMode(indNoOilp, OUTPUT);
  
  digitalWrite(indLgtPrk, HIGH);
  digitalWrite(indLgtLow, HIGH);
  digitalWrite(indLgtHgh, HIGH);
  digitalWrite(indBlnLft, HIGH);
  digitalWrite(indBlnRgt, HIGH);
  digitalWrite(indLgtBcn, HIGH);
  digitalWrite(indDifLoc, HIGH);
  digitalWrite(indHndBrk, HIGH);
  digitalWrite(indNoChrg, HIGH);
  digitalWrite(indNoOilp, HIGH);

  delay(500);

  digitalWrite(indLgtPrk, LOW);
  digitalWrite(indLgtLow, LOW);
  digitalWrite(indLgtHgh, LOW);
  digitalWrite(indBlnLft, LOW);
  digitalWrite(indBlnRgt, LOW);
  digitalWrite(indLgtBcn, LOW);
  digitalWrite(indDifLoc, LOW);
  digitalWrite(indHndBrk, LOW);
  digitalWrite(indNoChrg, LOW);
  digitalWrite(indNoOilp, LOW);

  Serial.begin(9600);
  delay(50);



}

void loop() {

  if (Serial.available() > 0) {         // incoming message handling
    msg = Serial.readStringUntil('\n');

    if (msg == 'hndshk') {
      Serial.println("hndshkresp");
    }

    if (msg == "indBlnOff") {
      digitalWrite(indBlnLft, LOW);
      digitalWrite(indBlnRgt, LOW);
    }

    if (msg == "indBlnLftOn") {
      digitalWrite(indBlnLft, HIGH);
      digitalWrite(indBlnRgt, LOW);
    }

    if (msg == "indBlnRgtOn") {
      digitalWrite(indBlnLft, LOW);
      digitalWrite(indBlnRgt, HIGH);
    }

    if (msg == "indHzdOn") {
      digitalWrite(indBlnLft, HIGH);
      digitalWrite(indBlnRgt, HIGH);
    }

  pinIo(indLgtPrk, "indLgtPrkOn", "indLgtPrkOff");
  pinIo(indLgtLow, "indLgtLowOn", "indLgtLowOff");
  pinIo(indLgtHgh, "indLgtHghOn", "indLgtHghOff");
  pinIo(indLgtBcn, "indLgtBcnOn", "indLgtBcnOff");
  pinIo(indHndBrk, "indHndBrkOn", "indHndBrkOff");
  pinIo(indNoChrg, "indNoChrgOn", "indNoChrgOff");
  pinIo(indNoOilp, "indNoOilpOn", "indNoOilpOff");

  }


}
