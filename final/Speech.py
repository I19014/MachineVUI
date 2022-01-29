import gpiozero
import argparse
import os
import queue
import sys
import json
import sounddevice as sd
import vosk
import threading
import time
import RPi.GPIO as GPIO
import simpleaudio as sa
from Activities import Activities
import simpleaudio as sa

class Speech: 
    
    STARTCODE = 'computer'
    def __init__(self,startcode):
        self.STARTCODE = startcode
    # Unsere Thread Funktion
    def thread_timer(self):
        # Aktiviere GPIO 17, um die grüne LED zum Leuchten zu bringen. 
        led = gpiozero.LED(17)
        self.power_gpio(17,led)
        # warte 10 Sekunden
        time.sleep(10)
        # Schalte die grüne LED wieder aus.
        self.close_gpio(17,led)

    def gpio_Input(self):
        #Statusausgabe bei Eingangssignal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(19, GPIO.IN)
        filename = 'audio/SystemStart.wav'
        wave_object = sa.WaveObject.from_wave_file(filename)
        while True:
            if GPIO.input(19) == 0:
                pass
            else:
                play_obj = wave_object.play()
                play_obj.wait_done() 

    def audio_Start(self):
        filename = 'audio/SystemStart.wav'
        self.play_Audio(filename)

    def success_Sound(self):
        filename = 'audio/Success.wav'
        self.play_Audio(filename)

    def fail_Sound(self):
        filename = 'audio/Fail.wav'
        self.play_Audio(filename)

    def play_Audio(self, audio):
        filename = audio
        wave_object = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_object.play()
        play_obj.wait_done() 
        
    # Definieren der Aktivierungsphase. Solange der thread gestartet ist, können Kommandos zum triggern der Methoden aus der Activities Klasse gesagt werden.
    # 
    def active(self,rec):
        print("active")
        # Thread definieren
        t = threading.Thread(target=self.thread_timer)
        # Thread starten
        t.start()
        i=0
        # solange Thread aktiv
        while t.is_alive():
            print('call a command')
            # hole die Daten aus der Queue, bzw. aus dem Stream
            data = q.get()
            if rec.AcceptWaveform(data):
                print("second record")
                # 
                res = json.loads(rec.Result())
                if 'Weiter'.upper() in res['text'].upper():
                    Speech.success_Sound()
                    Activities.impuls(18)
                    #t.Join()
                    break
                elif 'Start'.upper() in res['text'].upper():
                    Speech.success_Sound()
                    Activities.impuls(23)
                    #t.Join()
                    break
                print(res['text'])

    def power_gpio(self,GPIO,led):
        print(f"Power {GPIO}")
        try:
            # switch LED on
            if not led.is_lit:
                led.on()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))
    
    def close_gpio(self,GPIO,led):
        print(f"Close {GPIO}")
        try:
            # switch LED off
            if led.is_lit:
                led.off()
        # if any error occurs call exception
        except gpiozero.GPIOZeroError as err:
            print("Error occured: {0}".format(err))