#include <Button.h>

// Define inputs
#define serial0 0
#define serial1 1

Button emergency(2);        // Note: The software emergency and the desync buttons are for completely different occurences.
Button retOff(3);
Button retPos1(4);
Button retPos2(5);
Button retPos3(6);
Button retPos4(7);
Button engBrk(8);
Button lgtOff(9);
Button lgtPrk(10);
Button lgtLow(11);
Button lgtHgh(12);
Button blnLft(13);
Button blnRgt(14);
Button wipOff(15);
Button wipSpd1(16);
Button wipSpd2(17);
Button wipSpd3(18);
Button elcOff(19);
Button elcIgn(20);
Button engSrt(21);
Button trdWhl(22);
Button lgtBcn(23);
Button lgtHzd(24);
Button difLoc(25);
Button hndBrk(26);
Button winLdn(27);
Button winLup(28);
Button winRdn(29);
Button winRup(30);
Button susFrtUp(41);
Button susFrtDn(42);
Button susBckUp(43);
Button susBckDn(44);
Button susReset(47);
Button truAxl(45);
Button trlAxl(46);
Button deSync(52);

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

void softwareEmergency() {
  digitalWrite(indNoOilp, HIGH);
  while (1) {
    delay(9999);
  }
}

void setup() {

  // pin setup
  emergency.begin();
  retOff.begin();
  retPos1.begin();
  retPos2.begin();
  retPos3.begin();
  retPos4.begin();
  engBrk.begin();
  lgtOff.begin();
  lgtPrk.begin();
  lgtLow.begin();
  lgtHgh.begin();
  blnLft.begin();
  blnRgt.begin();
  wipOff.begin();
  wipSpd1.begin();
  wipSpd2.begin();
  wipSpd3.begin();
  elcOff.begin();
  elcIgn.begin();
  engSrt.begin();
  trdWhl.begin();
  lgtBcn.begin();
  lgtHzd.begin();
  difLoc.begin();
  hndBrk.begin();
  winLdn.begin();
  winLup.begin();
  winRdn.begin();
  winRup.begin();
  susFrtUp.begin();
  susFrtDn.begin();
  susBckUp.begin();
  susBckDn.begin();
  susReset.begin();
  truAxl.begin();
  trlAxl.begin();
  deSync.begin();

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

  if (emergency.read() == Button::PRESSED) {
    digitalWrite(indBlnLft, HIGH);
    digitalWrite(indBlnRgt, HIGH);
    softwareEmergency();
  }

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

  // end of message receiver block

  // start of message sending block

  if (deSync.read() == Button::RELEASED) {            // Desync button check. The whole part onyl runs if the desync button is released.




  }

}