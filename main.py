from gpiozero import TonalBuzzer, LED, Button
from gpiozero.tones import Tone
import firebase_admin
from firebase_admin import credentials, firestore
from signal import pause
import constant
from time import *
import time

cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

t = TonalBuzzer(26)
v1 = ["G4", "G4", "G4", "D4", "E4", "E4", "D4"]
v2 = ["B4", "B4", "A4", "A4", "G4"]
v3 = ["D4", "G4", "G4", "G4", "D4", "E4", "E4", "D4"]
song = [v1,v2,v3,v2]

a = LED(22)
b = LED(27)
c = LED(17)
d = LED(4)
e = LED(18)
f = LED(23)
g = LED(24)
h = LED(25)
i = LED(12)
j = LED(21)

greenLed = LED(19)

leds = [a,b,c,d,e,f,g,h,i,j]

for led in leds:
            led.off()

def on_timedatadoc_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print(f'Received document snapshot: {doc.to_dict()}')
        alarm_status = doc.to_dict()["alarm"]
        timer_status = doc.to_dict()["timeLeft"]
        print(f'alarm {alarm_status}')
        print(f'timeLeft {timer_status}')
        if timer_status != None:
            if timer_status > 10:
                blinkGreen()
        if timer_status == 10:
            a.on()
        if timer_status == 9:
            b.on()
        if timer_status == 8:
            c.on()
        if timer_status == 7:
            d.on()
        if timer_status == 6:
            e.on()
        if timer_status == 5:
            f.on()
        if timer_status == 4:
           g.on()
        if timer_status == 3:
            h.on()
        if timer_status == 2:
            i.on()
        if timer_status == 1:
           j.on()
        if timer_status == 0:
            soundBuzzer()            
        
doc_timedata_ref = db.collection(constant.COLLECTION_NAME).document(constant.TIMEDATA)
doc_timedata_watch = doc_timedata_ref.on_snapshot(on_timedatadoc_snapshot)

doc_timedata_ref.update({u'timeLeft': None})
doc_timedata_ref.update({u'alarm': None})

def blinkGreen():
    greenLed.on()
    sleep(.5)
    greenLed.off()  

def soundBuzzer():
    print("BUZZ")
    for led in leds:
            led.off()
    for verse in song:
        for note in verse:
            t.play(note)
            sleep(0.4)
            t.stop()
            sleep(0.1)
        sleep(0.2)
pause()