from functions import (getSwitch, getButton)

class keys:
    class Switches:
        class Retarder:
            def __init__(self):
                self.retOffKey = getSwitch('Retarder', 'retOffKey')
                self.retPos1Key = getSwitch('Retarder', 'retPos1Key')
                self.retPos2Key = getSwitch('Retarder', 'retPos2Key')
                self.retPos3Key = getSwitch('Retarder', 'retPos3Key')
                self.retPos4Key = getSwitch('Retarder', 'retPos4Key')

        class Lights:
            def __init__(self):
                self.lgtOffKey = getSwitch('Lights', 'lgtOffKey')
                self.lgtPrkKey = getSwitch('Lights', 'lgtPrkKey')
                self.lgtLowKey = getSwitch('Lights', 'lgtPrkKey')
                self.lgtHghKey = getSwitch('Lights', 'lgtHghKey')

        class Blinkers:
            def __init__(self):
                self.blnLftKey = getSwitch('Blinkers', 'blnLftKey')
                self.blnRgtKey = getSwitch('Blinkers', 'blnRgtKey')

        class Wipers:
            def __init__(self):
                self.wipOffKey = getSwitch('Wipers', 'wipOffKey')
                self.wipSpd1Key = getSwitch('Wipers', 'wipSpd1Key')
                self.wipSpd2Key = getSwitch('Wipers', 'wipSpd2Key')
                self.wipSpd3Key = getSwitch('Wipers', 'wipSpd3Key')

        class Ignition:
            def __init__(self):
                self.elcOffKey = getSwitch('Ignition', 'elcOffKey')
                self.elcIgnKey = getSwitch('Ignition', 'elcIgnKey')
                self.engSrtKey = getSwitch('Ignition', 'engSrtKey')

        class Switchboard:
            def __init__(self):
                self.trdWhlKey = getSwitch('Switchboard', 'trdWhlKey')
                self.lgtBcnKey = getSwitch('Switchboard', 'lgtBcnKey')
                self.lgtHzdKey = getSwitch('Switchboard', 'lgtHzdKey')
                self.difLocKey = getSwitch('Switchboard', 'difLocKey')
                self.hndBrkKey = getSwitch('Switchboard', 'hndBrkKey')

    class Buttons:
        class Switchboard:
            def __init__(self):
                self.engBrkKey = getButton('Switchboard', 'engBrkKey')
                self.truAxlKey = getButton('Switchboard', 'truAxlKey')
                self.trlAxlKey = getButton('Switchboard', 'trlAxlKey')

        class Windows:
            def __init__(self):
                self.winLdnKey = getButton('Windows', 'winLdnKey')
                self.winLupKey = getButton('Windows', 'winLupKey')
                self.winRdnKey = getButton('Windows', 'winRdnKey')
                self.winRupKey = getButton('Windows', 'winRupKey')

        class Suspension:
            def __init__(self):
                self.susFrtUpKey = getButton('Suspension', 'susFrtUpKey')
                self.susFrtDnKey = getButton('Suspension', 'susFrtDnKey')
                self.susBckUpKey = getButton('Suspension', 'susBckUpKey')
                self.susBckDnKey = getButton('Suspension', 'susBckDnKey')
                self.susResetKey = getButton('Suspension', 'susResetKey')