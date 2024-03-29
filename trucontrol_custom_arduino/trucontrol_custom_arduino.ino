// for version 0.1.4

#include <Button.h>
#include <HardwareSerial.h>

// Define inputs
#define serial0 0
#define serial1 1

Button emergency(7);        // Note: The software emergency and the desync buttons are for completely different occurences.
Button retOff(6);           // type: Rotary common GND
Button retPos1(5);
Button retPos2(4);
Button retPos3(3);
Button retPos4(8);
Button engBrk(2);           // type: Button  OnPress, onRelease
Button lgtOff(11);           // type: Rotary common GND
Button lgtPrk(10);
Button lgtLow(9);
Button lgtHgh(12);          // type: Switch  OnPress, onRelease
Button blnLft(13);          // type: Switch  OnPress, onRelease
Button blnRgt(14);
Button wipOff(15);          // type: Rotary common GND
Button wipSpd1(16);
Button wipSpd2(17);
Button wipSpd3(18);
//Button elcOff(0);          // type: Ignition common GND - Not in use anymore
Button elcIgn(36);
Button engSrt(37);
Button trdWhl(38);          // type: Switch  OnPress, onRelease
Button lgtBcn(39);          // type: Switch  OnPress, onRelease
Button lgtHzd(40);          // type: Switch  OnPress, onRelease
Button difLoc(41);          // type: Switch  OnPress, onRelease
Button hndBrk(42);          // type: Switch  OnPress, onRelease
Button winLdn(43);          // type: Button  OnPress, onRelease
Button winLup(44);          // type: Button  OnPress, onRelease
Button winRdn(45);          // type: Button  OnPress, onRelease
Button winRup(46);          // type: Button  OnPress, onRelease
Button susFrtUp(47);        // type: Button  OnPress, onRelease
Button susFrtDn(48);        // type: Button  OnPress, OnRelease
Button susBckUp(49);        // type: Button  OnPress, OnRelease
Button susBckDn(50);        // type: Button  OnPress, OnRelease
Button susReset(53);        // type: Button  OnPress
Button truAxl(51);          // type: Button  OnPress
Button trlAxl(52);          // type: Button  OnPress
Button deSync(54);

// Define outputs
#define indLgtPrk 19
#define indLgtLow 20
#define indLgtHgh 21
#define indBlnLft 22
#define indBlnRgt 23
#define indLgtBcn 24
#define indDifLoc 25
#define indHndBrk 26
#define indNoChrg 27
#define indNoOilp 28
#define indLgtHzd 29
#define indAirLow 30
#define indFueLow 31
#define indChcEng 32
#define indRetard 33
#define indCruise 34
#define indWatTem 35

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
  digitalWrite(indHndBrk, HIGH);
  delay(500);
  digitalWrite(indHndBrk, LOW);
  delay(500);
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
  //elcOff.begin();
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
  pinMode(indAirLow, OUTPUT);
  pinMode(indLgtHzd, OUTPUT);
  pinMode(indFueLow, OUTPUT);
  pinMode(indChcEng, OUTPUT);
  pinMode(indRetard, OUTPUT);
  pinMode(indCruise, OUTPUT);
  pinMode(indWatTem, OUTPUT);
  
  digitalWrite(indLgtPrk, HIGH);      // LED test
  digitalWrite(indLgtLow, HIGH);
  digitalWrite(indLgtHgh, HIGH);
  digitalWrite(indBlnLft, HIGH);
  digitalWrite(indBlnRgt, HIGH);
  digitalWrite(indLgtBcn, HIGH);
  digitalWrite(indDifLoc, HIGH);
  digitalWrite(indHndBrk, HIGH);
  digitalWrite(indNoChrg, HIGH);
  digitalWrite(indNoOilp, HIGH);
  digitalWrite(indAirLow, HIGH);
  digitalWrite(indLgtHzd, HIGH);
  digitalWrite(indFueLow, HIGH);
  digitalWrite(indChcEng, HIGH);
  digitalWrite(indRetard, HIGH);
  digitalWrite(indCruise, HIGH);
  digitalWrite(indWatTem, HIGH);

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
  digitalWrite(indAirLow, LOW);
  digitalWrite(indLgtHzd, LOW);
  digitalWrite(indFueLow, LOW);
  digitalWrite(indChcEng, LOW);
  digitalWrite(indRetard, LOW);
  digitalWrite(indCruise, LOW);
  digitalWrite(indWatTem, LOW);

  if (emergency.read() == Button::PRESSED) {
    digitalWrite(indBlnLft, HIGH);
    digitalWrite(indBlnRgt, HIGH);
    softwareEmergency();
  }

  Serial.begin(9600);
  delay(50);

  digitalWrite(indLgtPrk, HIGH);        // indicating that the program is starting
  digitalWrite(indLgtLow, HIGH);
  delay(500);
  digitalWrite(indLgtPrk, LOW);
  digitalWrite(indLgtPrk, LOW);
}

void loop() {

  if (Serial.available() > 0) {         // incoming message handling
    msg = Serial.readStringUntil('\n');

    if (msg == "hndshk") {
      Serial.println("hndshkresp");
    }

    if (msg == "indBlnOff") {
      digitalWrite(indBlnLft, LOW);
      digitalWrite(indBlnRgt, LOW);
      digitalWrite(indLgtHzd, LOW);
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
      digitalWrite(indLgtHzd, HIGH);
    }

    pinIo(indLgtPrk, "indLgtPrkOn", "indLgtPrkOff");
    pinIo(indLgtLow, "indLgtLowOn", "indLgtLowOff");
    pinIo(indLgtHgh, "indLgtHghOn", "indLgtHghOff");
    pinIo(indLgtBcn, "indLgtBcnOn", "indLgtBcnOff");
    pinIo(indHndBrk, "indHndBrkOn", "indHndBrkOff");
    pinIo(indNoChrg, "indNoChrgOn", "indNoChrgOff");
    pinIo(indNoOilp, "indNoOilpOn", "indNoOilpOff");
    pinIo(indAirLow, "indAirLowOn", "indAirLowOff");
    pinIo(indFueLow, "indFueLowOn", "indFueLowOff");
    pinIo(indChcEng, "indChcEngOn", "indChcEngOff");
    pinIo(indRetard, "indRetardOn", "indRetardOff");
    pinIo(indCruise, "indCruiseOn", "indCruiseOff");
    pinIo(indWatTem, "indWatTemOn", "indWatTemOff");

  }

  // end of message receiver block

  // start of message sending block

  if (deSync.read() == Button::RELEASED) {
    
    if (deSync.released()) {
      digitalWrite(indNoOilp, LOW);
      digitalWrite(indNoChrg, LOW);
      digitalWrite(indLgtPrk, LOW);
      digitalWrite(indLgtLow, LOW);
    }

    //retarder
    if (retOff.pressed()) {
      Serial.println("retOff");
    }
    if (retPos1.pressed()) {
      Serial.println("retPos1");
    }
    if (retPos2.pressed()) {
      Serial.println("retPos2");
    }
    if (retPos3.pressed()) {
      Serial.println("retPos3");
    }
    if (retPos4.pressed()) {
      Serial.println("retPos4");
    }

    // engine brake
    if (engBrk.pressed()) {
      Serial.println("engBrkOn");
    }
    if (engBrk.released()) {
      Serial.println("engBrkOff");
    }

    // lights (except high beam)
    if (lgtOff.pressed()) {
      Serial.println("lgtOff");
    }
    if (lgtPrk.pressed()) {
      Serial.println("lgtPrk");
    }
    if (lgtLow.pressed()) {
      Serial.println("lgtLow");
    }

    // high beams
    if (lgtHgh.pressed() || lgtHgh.released()) {
      Serial.println("lgtHgh");
    }

    // blinkers
    if (blnLft.pressed()) {
      Serial.println("blnLftOn");
    }
    if (blnLft.released()) {
      Serial.println("blnLftOff");
    }
    if (blnRgt.pressed()) {
      Serial.println("blnRgtOn");
    }
    if (blnRgt.released()) {
      Serial.println("blnRgtOff");
    }

    // wipers
    if(wipOff.pressed()) {
      Serial.println("wipOff");
    }
    if (wipSpd1.pressed()) {
      Serial.println("wipSpd1");
    }
    if (wipSpd2.pressed()) {
      Serial.println("wipSpd2");
    }
    if (wipSpd3.pressed()) {
      Serial.println("wipSpd3");
    }

    // electrics/ignition/start
    if (elcIgn.released()) {                      // Function changed from using a dedicated ignition off pin
      Serial.println("elcOff");
    }
    if (elcIgn.pressed()) {
      Serial.println("elcIgn");
    }
    if (engSrt.pressed()) {
      Serial.println("engSrt");
    }

    // trailer/third wheel attach/detach
    if (trdWhl.pressed() || trdWhl.released()) {
      Serial.println("trdWhl");
    }

    // beacons
    if (lgtBcn.pressed() || lgtBcn.released()) {
      Serial.println("lgtBcn");
    }

    // hazards
    if (lgtHzd.pressed() || lgtHzd.released()) {
      Serial.println("lgtHzd");
    }

    // difflock + indicator handling
    if (difLoc.pressed()) {
      Serial.println("difLoc");
      digitalWrite(indDifLoc, HIGH);
    }
    if (difLoc.released()) {
      Serial.println("difLoc");
      digitalWrite(indDifLoc, LOW);
    }
    
    // handbrake
    if (hndBrk.pressed() || hndBrk.released()) {
      Serial.println("hndBrk");
    }

    // left window
    if (winLdn.pressed()) {
      Serial.println("winLdnOn");
    }
    if (winLdn.released()) {
      Serial.println("winLdnOff");
    }
    if (winLup.pressed()) {
      Serial.println("winLupOn");
    }
    if (winLup.released()) {
      Serial.println("winLupOff");
    }

    // right window
    if (winRdn.pressed()) {
      Serial.println("winRdnOn");
    }
    if (winRdn.released()) {
      Serial.println("winRdnOff");
    }
    if (winRup.pressed()) {
      Serial.println("winRupOn");
    }
    if (winRup.released()) {
      Serial.println("winRupOff");
    }

    // front suspension
    if (susFrtUp.pressed()) {
      Serial.println("susFrtUpOn");
    }
    if (susFrtUp.released()) {
      Serial.println("susFrtUpOff");
    }
    if (susFrtDn.pressed()) {
      Serial.println("susFrtDnOn");
    }
    if (susFrtDn.released()) {
      Serial.println("susFrtDnOff");
    }

    // rear suspension (for some reason I used back in the software handles smh...)
    if (susBckUp.pressed()) {
      Serial.println("susBckUpOn");
    }
    if (susBckUp.released()) {
      Serial.println("susBckUpOff");
    }
    if (susBckDn.pressed()) {
      Serial.println("susBckDnOn");
    }
    if (susBckDn.released()) {
      Serial.println("susBckDnOff");
    }

    // suspension reset                 Help, the IDE is using up all of my RAM and is becoming sentient
    if (susReset.pressed()) {
      Serial.println("susReset");
    }

    // truck axle
    if (truAxl.pressed()) {
      Serial.println("truAxl");
    }

    // trailer axle
    if (trlAxl.pressed()) {
      Serial.println("trlAxl");
    }

  } else if (deSync.read() == Button::PRESSED) {
    digitalWrite(indNoOilp, HIGH);
    digitalWrite(indNoChrg, HIGH);
    digitalWrite(indLgtLow, HIGH);
    delay(100);
    digitalWrite(indLgtLow, LOW);
    delay(100);
  }
  
  // Switching to VScode did help. :-)

}
